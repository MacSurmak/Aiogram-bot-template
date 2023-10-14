from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def add_user(session: AsyncSession, user_id: int, username: str, name: str):
    user = User(user_id=user_id, username=username, name=name)
    session.add(user)
    await session.commit()


async def get_id(session: AsyncSession):
    selection = select(User.user_id).where(User.receive_mail.is_(True))
    result = await session.execute(selection)
    ids = []
    for i in result:
        ids.append(i[0])
    return ids


async def get_message_id(session: AsyncSession, user_id):
    selection = select(User.old_message).where(User.user_id == user_id)
    result = await session.execute(selection)
    return result.scalars().one()


async def save_message_id(session: AsyncSession, user_id, message_id):
    selection = select(User).where(User.user_id == user_id)
    result = await session.execute(selection)
    user = result.scalars().one()
    user.old_message = message_id
    await session.commit()


async def update_subscription_status(session: AsyncSession, user_id, status: bool):
    selection = select(User).where(User.user_id == user_id)
    result = await session.execute(selection)
    user = result.scalars().one()
    user.receive_mail = status
    await session.commit()
