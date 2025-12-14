from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("ℹ️ Сейчас нет активного действия.")
        return

    await state.clear()
    await message.answer("❌ Действие отменено.")