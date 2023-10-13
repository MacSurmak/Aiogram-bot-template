from typing import Callable, Awaitable, Dict, Any

import imaplib

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ImapMiddleware(BaseMiddleware):
    def __init__(self, imap_client):
        super().__init__()
        self.imap_client = imap_client

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        with self.imap_client as imap:
            data["imap"] = imap
            return await handler(event, data)
