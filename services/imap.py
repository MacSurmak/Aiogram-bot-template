import asyncio
from aioimaplib import aioimaplib


async def check_mailbox(host, user, password):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()
    await imap_client.login(user, password)
    mes = await imap_client.select("INBOX")
    print(mes)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    check_mailbox('imap.mail.ru',
                  'group.317.2022@mail.ru',
                  'i7U1KaCjZG5NVn4zs9EU'))
