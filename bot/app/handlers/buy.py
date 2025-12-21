import logging
logger = logging.getLogger(__name__)

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.api.backend import BackendAPI
from app.keyboards.common import main_menu

router = Router()
api = BackendAPI()


@router.message(F.text == "🛍 Купить")
async def buy_handler(message: Message, state: FSMContext, user_id: int):
    """
    Обработчик кнопки 'Купить' - показывает список товаров для покупки
    """
    await state.clear()
    
    try:
        logger.info("Buy action triggered: user_id=%s", user_id)
        
        # Получить товары из backend
        products = await api.list_products(section="market")
        
        if not products:
            await message.answer(
                "😔 В данный момент нет товаров на продажу.\n\n"
                "Попробуйте позже или добавьте свой товар!"
            )
            return
        
        # Форматировать список товаров
        response_text = f"🛍 Товары на продажу ({len(products)} шт.):\n\n"
        
        for idx, product in enumerate(products, 1):
            seller_username = product.get('seller_username', 'Неизвестно')
            product_info = (
                f"{idx}. {product['title']}\n"
                f"   💰 Цена: {product['price']} ₽\n"
                f"   📝 {product.get('description', 'Без описания')[:50]}\n"
                f"   👤 Продавец: @{seller_username}\n"
            )
            response_text += product_info
        
        response_text += (
            "\n\n💬 Для покупки напишите продавцу в Telegram.\n"
            "Система сделок в разработке."
        )
        
        kb = main_menu()
        await message.answer(response_text, reply_markup=kb)
        
        logger.info("Buy list sent: user_id=%s products_count=%s", user_id, len(products))
        
    except Exception as e:
        logger.exception("Error in buy_handler: %s", e)
        await message.answer(
            "❌ Ошибка при загрузке товаров.\n"
            "Попробуйте позже."
        )
