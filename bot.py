import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_data import config
from handlers import commands, user, admin
from keyboards.commands_menu import set_commands_menu
from middlewares import DbSessionMiddleware, GetLangMiddleware
from database import Base
from services import setup_logger


async def main() -> None:
    engine = create_async_engine(url=config.db.url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    redis: Redis = Redis(host=config.redis.host, port=config.redis.port, password=config.redis.password)
    storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token=config.bot.token,
                   parse_mode='HTML')

    dp: Dispatcher = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(GetLangMiddleware())
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(commands.router)
    dp.include_router(user.router)
    dp.include_router(admin.router)

    await set_commands_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    setup_logger("INFO")
    asyncio.run(main())
