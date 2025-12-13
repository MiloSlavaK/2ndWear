from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, user: dict):
    await message.answer(
        "👋 Добро пожаловать в 2ndWear.\n\n"
        "Профиль успешно зарегистрирован."
    )
