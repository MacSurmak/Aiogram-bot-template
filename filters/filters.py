from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import User

from config_data import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message = None, callback: CallbackQuery = None) -> bool:
        if message:
            return message.from_user.id in config.bot.admin_ids
        elif callback:
            print("call")
            return callback.from_user.id in config.bot.admin_ids


class IsRegistered(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        result = await session.execute(select(User.user_id))
        ids = result.scalars().all()
        return message.from_user.id in ids
