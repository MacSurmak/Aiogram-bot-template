import aioimaplib
import asyncio
import email
from email.header import decode_header
import base64
import codecs
import os

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import FSInputFile, InputMediaDocument

from sqlalchemy.ext.asyncio import async_sessionmaker
from database import get_id
from lexicon.lexicon import lexicon


async def message_processing(msg) -> (str, list[str]):
    # get sender
    try:
        sender_name = decode_header(msg["From"])[0][0].decode()
    except (AttributeError, TypeError):
        sender_name = msg["From"]
    sender_name = sender_name.replace("<", "&lt;").replace(">", "&gt;")
    sender_mail = msg["Return-path"].replace("<", "&lt;").replace(">", "&gt;")

    # get header
    try:
        header = decode_header(msg["Subject"])[0][0].decode()
    except (AttributeError, TypeError):
        header = msg["Subject"]
    if header is not None:
        header = header.replace("<", "&lt;").replace(">", "&gt;")
    else:
        header = "&lt;No subject&gt;"

    # get text
    text = ""
    for part in msg.walk():
        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            try:
                text = text + codecs.decode(base64.b64decode(part.get_payload()), encoding='utf-8',
                                            errors='replace')
            except (AttributeError, TypeError):
                text = text + str(base64.b64decode(part.get_payload()))
    text = text.replace("<", "&lt;").replace(">", "&gt;")

    message = lexicon("ru", 'send-mail').format(sender_name=sender_name,
                                                sender_mail=sender_mail,
                                                header=header,
                                                underline=(len(header)) * "--",
                                                text=text)

    # get attachments
    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            decoded_filename = decode_header(filename)[0][0].decode()
            att_path = os.path.join("Attachments", decoded_filename)
            open(att_path, 'wb').write(part.get_payload(decode=True))
            att_input = FSInputFile(att_path)
            if len(message) < 1024 and not attachments:
                att_input = InputMediaDocument(media=att_input, caption=message)
                message = ""
            else:
                att_input = InputMediaDocument(media=att_input)
            attachments.append(att_input)
    return message, attachments


async def wait_for_new_message(host, user, password, bot: Bot, session_maker: async_sessionmaker):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()

    await imap_client.login(user, password)
    await imap_client.select()

    while True:

        idle = await imap_client.idle_start(timeout=60)

        mail = await imap_client.wait_server_push()
        mail = mail[0].decode("utf-8")

        imap_client.idle_done()
        await asyncio.wait_for(idle, 30)

        if 'EXISTS' in mail:
            mail_id = str(mail).split()[0]
            print(mail_id)

            # fetch mail
            res, msg = await imap_client.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg[1])
            message, attachments = await message_processing(msg)

            async with session_maker() as session:
                ids = await get_id(session)

            for chat_id in ids:
                try:
                    if not message:
                        result = await bot.send_media_group(chat_id=chat_id,
                                                            media=attachments)
                    else:
                        await bot.send_message(chat_id=chat_id,
                                               text=message)
                        result = await bot.send_media_group(chat_id=chat_id,
                                                            media=attachments)
                    pass
                except Exception as e:
                    print(e)
                    pass
