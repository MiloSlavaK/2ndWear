from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.constants import CLOTHING_CATEGORIES, SIZES, SHOE_SIZES, COLORS, STYLES, GENDERS, CONDITIONS


def contact_request_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить контакт", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def categories_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in CLOTHING_CATEGORIES],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def sizes_kb(category: str | None = None) -> ReplyKeyboardMarkup:
    # Для обуви используем числовые размеры
    sizes = SHOE_SIZES if category == "Обувь" else SIZES
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=size)] for size in sizes],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def colors_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=color)] for color in COLORS],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def styles_kb() -> ReplyKeyboardMarkup:
    # Формируем ряды по 2 позиции для компактности
    rows = []
    for i in range(0, len(STYLES), 2):
        row = [KeyboardButton(text=STYLES[i])]
        if i + 1 < len(STYLES):
            row.append(KeyboardButton(text=STYLES[i + 1]))
        rows.append(row)
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def genders_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=gender)] for gender in GENDERS],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def conditions_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cond)] for cond in CONDITIONS],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def sections_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="market")],
            [KeyboardButton(text="swop")],
            [KeyboardButton(text="charity")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
