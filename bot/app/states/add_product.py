from aiogram.fsm.state import State, StatesGroup


class AddProductState(StatesGroup):
    title = State()
    price = State()
    description = State()
    category = State()
    size = State()
    color = State()
    style = State()
    gender = State()
    condition = State()
    section = State()
    photo = State()
    confirm = State()
