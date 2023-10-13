import aioimaplib
import asyncio
import email
from email.header import decode_header
import base64
import codecs
import re
from aiogram.exceptions import TelegramForbiddenError

from aiogram import Bot

from config_data import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database import Base, get_id
from lexicon.lexicon import lexicon


async def message_processing(msg) -> str:
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
        header = "Без темы"

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
    return message


async def wait_for_new_message(host, user, password, bot: Bot, session_maker: async_sessionmaker):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()
    await imap_client.login(user, password)
    await imap_client.select()

    mail_id = None
    while True:
        idle = await imap_client.idle_start(timeout=60)

        async with session_maker() as session:
            ids = await get_id(session)

        mail = await imap_client.wait_server_push()
        mail = mail[0].decode("utf-8")
        if 'EXISTS' in mail:
            mail_id = str(mail).split()[0]
            imap_client.idle_done()
            break

    if mail_id is not None:

        # fetch mail
        res, msg = await imap_client.fetch(mail_id, '(RFC822)')
        msg = email.message_from_bytes(msg[1])
        message = await message_processing(msg)

        for chat_id in ids:
            try:
                await bot.send_message(chat_id=chat_id,
                                       text=message)
            except TelegramForbiddenError:
                pass

    await asyncio.wait_for(idle, 30)
