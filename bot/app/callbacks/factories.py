from aiogram.filters.callback_data import CallbackData


class ProductCallback(CallbackData, prefix="product"):
    action: str
    product_id: int
