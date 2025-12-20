from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.keyboards.common import main_menu

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, user: dict | None = None):
    if user is None:
        await message.answer(
            "⚠️ Сервис временно недоступен. Попробуйте позже."
        )
        return
    kb = main_menu()
    await message.answer(
        "👋 Добро пожаловать в 2ndWear.\n\n"
        "Профиль успешно зарегистрирован.", reply_markup=kb
    )
