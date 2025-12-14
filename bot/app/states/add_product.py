from aiogram.fsm.state import State, StatesGroup


class AddProductState(StatesGroup):
    title = State()
    price = State()
    description = State()
    category = State()
    photo = State()
    confirm = State()
