from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Mail


async def add_user(session: AsyncSession, user_id: int, username: str, name: str):
    user = User(user_id=user_id, username=username, name=name)
    session.add(user)
    await session.commit()


async def add_mail(session: AsyncSession, mail_id: int):
    mail = Mail(mail_id=mail_id)
    session.add(mail)
    await session.commit()


async def get_id(session: AsyncSession):
    selection = select(User.user_id)
    result = await session.execute(selection)
    ids = []
    for i in result:
        ids.append(i[0])
    return ids
