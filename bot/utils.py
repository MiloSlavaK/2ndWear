from aiogram import Bot
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

async def notify_user(user_telegram_id: int, message: str):
    await bot.send_message(chat_id=user_telegram_id, text=message)