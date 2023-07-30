from aiogram import Bot, Dispatcher
from config_data.config import load_config

config = load_config(".env")

bot: Bot = Bot(config.tg_bot.token)
dp: Dispatcher = Dispatcher()

if __name__ == '__main__':
    dp.run_polling(bot)
