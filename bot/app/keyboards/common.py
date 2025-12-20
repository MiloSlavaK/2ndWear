from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Добавить товар")],
            [KeyboardButton(text="🛍 Купить")],
        ],
        resize_keyboard=True
    )
