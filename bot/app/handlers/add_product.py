import logging
logger = logging.getLogger(__name__)

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from app.states.add_product import AddProductState

from app.api.backend import BackendAPI

router = Router()
api = BackendAPI()


@router.message(F.text == "📤 Добавить товар")
async def start_add_product(message: Message, state: FSMContext):
    
    await state.clear()
    await state.set_state(AddProductState.title)

    await message.answer(
        "📦 Добавление товара\n\n"
        "Введите название товара:\n\n"
        "Для отмены — /cancel"
    )
    logger.info("FSM AddProduct started: telegram_id=%s", message.from_user.id)


@router.message(AddProductState.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await state.set_state(AddProductState.price)
    await message.answer("💰 Введите цену (числом):")


@router.message(AddProductState.price)
async def add_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Цена должна быть числом. Введите ещё раз:")
        return

    await state.update_data(price=int(message.text))

    await state.set_state(AddProductState.description)
    await message.answer("📝 Введите описание товара:")


@router.message(AddProductState.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductState.category)
    await message.answer("🏷 Укажите категорию товара:")


@router.message(AddProductState.category)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddProductState.photo)
    await message.answer("📸 Отправьте фото товара:")


@router.message(AddProductState.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(image_url=photo_id)

    data = await state.get_data()

    text = (
        "🔎 Проверьте данные товара:\n\n"
        f"Название: {data['title']}\n"
        f"Цена: {data['price']} ₽\n"
        f"Описание: {data['description']}\n\n"
        "Подтвердить добавление?"
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await state.set_state(AddProductState.confirm)
    await message.answer_photo(photo_id, caption=text, reply_markup=keyboard)


@router.message(AddProductState.photo)
async def photo_required(message: Message):
    await message.answer("❌ Пожалуйста, отправьте фото товара.")


@router.message(AddProductState.confirm, F.text == "❌ Отменить")
async def confirm_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Добавление товара отменено.")


@router.message(AddProductState.confirm, F.text == "✅ Подтвердить")
async def confirm_add_product(message: Message, state: FSMContext, user_id: int):
    data = await state.get_data()
    seller_id = message.from_user.id  # временно, позже будет backend user_id
    try:
        product = await api.create_product(
            seller_id=user_id,
            data=data,
        )
    except Exception:
        await message.answer(
            "❌ Ошибка при сохранении товара.\n"
            "Попробуйте позже."
        )
        logger.exception("Failed to create product")
        return

    await state.clear()
    await message.answer(
        "✅ Товар подтверждён.\n\n"
        "На следующем этапе мы отправим его в backend."
    )
    logger.info(
        "FSM AddProduct confirmed: telegram_id=%s data=%s",
        message.from_user.id,
        data,
    )
