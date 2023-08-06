from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Key


async def add_user(session: AsyncSession, user_id: int):
    user = User(user_id=user_id)
    session.add(user)
    await session.commit()

