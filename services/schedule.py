import asyncio
import aioschedule
from aiogram import Router, Bot

router: Router = Router(name='schedule-router')


@router.message()
async def send_new_mail(bot: Bot, mail_id: int):
    await bot.send_message(chat_id=391102946,
                           text=f"{mail_id}")


async def scheduler():
    aioschedule.every().second.do(send_new_mail, mail_id=6)
    while True:
        await aioschedule.run_pending()
