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
    await message.answer("🏷 Укажите категорию товара (например: Одежда, Обувь, Аксессуары):")


@router.message(AddProductState.category)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    
    # Клавиатура с размерами
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="XS")],
            [KeyboardButton(text="S")],
            [KeyboardButton(text="M")],
            [KeyboardButton(text="L")],
            [KeyboardButton(text="XL")],
            [KeyboardButton(text="XXL")],
            [KeyboardButton(text="Не указан")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.size)
    await message.answer("📏 Выберите размер:", reply_markup=keyboard)


@router.message(AddProductState.size)
async def add_size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    
    # Клавиатура с цветами
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Чёрный"), KeyboardButton(text="Белый")],
            [KeyboardButton(text="Красный"), KeyboardButton(text="Синий")],
            [KeyboardButton(text="Зелёный"), KeyboardButton(text="Жёлтый")],
            [KeyboardButton(text="Серый"), KeyboardButton(text="Другой")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.color)
    await message.answer("🎨 Выберите цвет:", reply_markup=keyboard)


@router.message(AddProductState.color)
async def add_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Casual"), KeyboardButton(text="Formal")],
            [KeyboardButton(text="Sport"), KeyboardButton(text="Boho")],
            [KeyboardButton(text="Vintage"), KeyboardButton(text="Other")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.style)
    await message.answer("👗 Выберите стиль:", reply_markup=keyboard)


@router.message(AddProductState.style)
async def add_style(message: Message, state: FSMContext):
    await state.update_data(style=message.text)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
            [KeyboardButton(text="Унисекс"), KeyboardButton(text="Детский")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.gender)
    await message.answer("👥 Для кого:", reply_markup=keyboard)


@router.message(AddProductState.gender)
async def add_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отличное"), KeyboardButton(text="Хорошее")],
            [KeyboardButton(text="Нормальное"), KeyboardButton(text="Требует чистки")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.condition)
    await message.answer("✨ Состояние товара:", reply_markup=keyboard)


@router.message(AddProductState.condition)
async def add_condition(message: Message, state: FSMContext):
    await state.update_data(condition=message.text)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="market"), KeyboardButton(text="swop")],
            [KeyboardButton(text="charity")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(AddProductState.section)
    await message.answer("📂 Выберите раздел:\n• market - продажа\n• swop - обмен\n• charity - бесплатно", reply_markup=keyboard)


@router.message(AddProductState.section)
async def add_section(message: Message, state: FSMContext):
    if message.text not in ["market", "swop", "charity"]:
        await message.answer("❌ Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(section=message.text)
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
        f"Описание: {data['description']}\n"
        f"Категория: {data['category']}\n"
        f"Размер: {data['size']}\n"
        f"Цвет: {data['color']}\n"
        f"Стиль: {data['style']}\n"
        f"Для: {data['gender']}\n"
        f"Состояние: {data['condition']}\n"
        f"Раздел: {data['section']}\n\n"
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
    """Отправить товар в backend"""
    data = await state.get_data()
    
    try:
        product = await api.create_product(
            seller_id=user_id,  # user_id из UserMiddleware
            data=data,
        )
        await state.clear()
        await message.answer(
            "✅ Товар успешно добавлен!\n\n"
            f"ID товара: {product['id']}\n"
            "Он уже доступен на нашем сайте."
        )
        logger.info(
            "FSM AddProduct completed: telegram_id=%s user_id=%s product_id=%s",
            message.from_user.id,
            user_id,
            product['id'],
        )
    except Exception as e:
        await message.answer(
            "❌ Ошибка при сохранении товара.\n"
            "Попробуйте позже или свяжитесь с поддержкой."
        )
        logger.exception("Failed to create product: user_id=%s error=%s", user_id, e)
        return
