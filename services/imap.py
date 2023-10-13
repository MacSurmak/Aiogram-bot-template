import aioimaplib
import asyncio
import email
from email.header import decode_header
import base64
import re

from aiogram import Bot

from config_data import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database import Base, get_id


async def wait_for_new_message(host, user, password, bot: Bot, session_maker: async_sessionmaker):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()
    await imap_client.login(user, password)
    await imap_client.select()

    while True:
        idle = await imap_client.idle_start(timeout=60)
        mail = await imap_client.wait_server_push()
        mail = mail[0].decode("utf-8")
        if 'EXISTS' in mail:
            async with session_maker() as session:
                ids = await get_id(session)
            mail_id = str(mail).split()[0]

            msg = await imap_client.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg[0][1])
            # letter_date = email.utils.parsedate_tz(msg["Date"])
            # letter_from = msg["Return-path"]
            # header = decode_header(msg["Subject"])[0][0].decode()
            for part in msg.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    print(base64.b64decode(part.get_payload()).decode())

            for chat_id in ids:
                await bot.send_message(chat_id=chat_id, text=f"{mail_id}")
        imap_client.idle_done()
        await asyncio.wait_for(idle, 30)
