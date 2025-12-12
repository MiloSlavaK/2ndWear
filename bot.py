import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from config import BOT_TOKEN, ADMIN_CHAT_ID, user_data_temp
from database import add_product
from config import BOT_TOKEN, ADMIN_CHAT_ID, user_data_temp, STYLES, COLORS

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
TITLE, PRICE, DESCRIPTION, STYLE, COLOR, PHOTO = range(6)


# Вспомогательные функции
async def moderate_product(product_id, status, context, query):
    """Одобрение/отклонение товара модератором"""
    with open('products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for product in data['products']:
        if product['id'] == product_id:
            product['status'] = status
            break

    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    status_text = "одобрен" if status == 'approved' else "отклонен"
    await query.edit_message_text(f"✅ Товар #{product_id} {status_text}")


async def contact_seller(product_id, context, query):
    """Покупатель хочет связаться с продавцом"""
    with open('products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    product = next((p for p in data['products'] if p['id'] == product_id), None)

    if not product:
        await query.answer("Товар не найден", show_alert=True)
        return

    seller_id = product.get('user_id')
    seller_username = product.get('username', 'Пользователь')

    # Сообщение покупателю
    await query.edit_message_text(
        f"✉️ *Связь с продавцом*\n\n"
        f"Товар: {product['title']}\n"
        f"Продавец: @{seller_username}\n\n"
        f"1. Напишите продавцу в Telegram\n"
        f"2. Укажите номер товара: #{product_id}\n"
        f"3. Обсудите детали покупки\n\n"
        f"⚠️ *Будьте осторожны!*\n"
        f"• Не переводите деньги заранее\n"
        f"• Используйте безопасные способы оплаты",
        parse_mode='Markdown'
    )

    # Уведомление продавцу
    try:
        await context.bot.send_message(
            chat_id=seller_id,
            text=f"👋 *Кто-то заинтересовался вашим товаром!*\n\n"
                 f"Товар: {product['title']}\n"
                 f"ID: #{product_id}\n\n"
                 f"Покупатель напишет вам в Telegram.\n"
                 f"Будьте на связи!",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Не удалось уведомить продавца: {e}")


# Основные функции бота
async def start(update: Update, context):
    # Создаем постоянное меню
    keyboard = [
        ["📤 Добавить товар"],
        ["📋 Мои товары", "🛍️ Купить"],
        ["ℹ️ Помощь", "👤 Профиль"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

    await update.message.reply_text(
        '👋 Добро пожаловать в 2ndWear!\n'
        'Продавайте и покупайте одежду с историей.',
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == 'add_item':
        await query.edit_message_text("📝 Введите название товара:")
        return TITLE

    elif query.data.startswith('style_'):
        # Обработка выбора стиля
        style_index = int(query.data.split('_')[1])
        selected_style = STYLES[style_index]
        style_name = selected_style.split('(')[0].strip()

        if user_id not in user_data_temp:
            user_data_temp[user_id] = {}

        # Сохраняем только один стиль
        user_data_temp[user_id]['style'] = style_name

        # Сразу переходим к выбору цвета
        keyboard = []
        for i in range(0, len(COLORS), 4):
            row = []
            for j in range(4):
                if i + j < len(COLORS):
                    color_text = COLORS[i + j].split(' ')[1]
                    row.append(InlineKeyboardButton(color_text, callback_data=f'color_{i + j}'))
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"✅ Стиль: {style_name}")
        await query.message.reply_text("🌈 Выберите ОДИН основной цвет:", reply_markup=reply_markup)
        return COLOR

    elif query.data.startswith('color_'):
        # Обработка выбора цвета
        color_index = int(query.data.split('_')[1])
        selected_color = COLORS[color_index]
        color_name = selected_color.split(' ')[1]

        user_data_temp[user_id]['color'] = color_name
        await query.edit_message_text(f"✅ Цвет: {color_name}")
        await query.message.reply_text("📸 Отправьте фото товара:")
        return PHOTO

    # Остальные обработчики...
    elif query.data == 'my_items':
        await query.edit_message_text("📋 Ваши товары (пока пусто)")

    elif query.data == 'help':
        await query.edit_message_text("ℹ️ Просто нажмите 'Добавить товар' и следуйте инструкциям.")

    elif query.data.startswith('approve_'):
        product_id = int(query.data.split('_')[1])
        await moderate_product(product_id, 'approved', context, query)

    elif query.data.startswith('reject_'):
        product_id = int(query.data.split('_')[1])
        await moderate_product(product_id, 'rejected', context, query)

    elif query.data.startswith('contact_'):
        product_id = int(query.data.split('_')[1])
        await contact_seller(product_id, context, query)


# Функции для добавления товара
async def get_title(update: Update, context):
    user_id = update.message.from_user.id
    user_data_temp[user_id] = {'title': update.message.text}
    await update.message.reply_text("💰 Укажите цену в рублях:")
    return PRICE


async def get_price(update: Update, context):
    try:
        price = int(update.message.text)
        user_id = update.message.from_user.id
        user_data_temp[user_id]['price'] = price
        await update.message.reply_text("📝 Напишите описание товара:")
        return DESCRIPTION
    except:
        await update.message.reply_text("❌ Введите число!")
        return PRICE


async def get_description(update: Update, context):
    user_id = update.message.from_user.id
    user_data_temp[user_id]['description'] = update.message.text

    # Показываем кнопки со стилями
    keyboard = []
    for i in range(0, len(STYLES), 3):
        row = []
        for j in range(3):
            if i + j < len(STYLES):
                style_text = STYLES[i + j].split('(')[0].strip()
                row.append(InlineKeyboardButton(style_text, callback_data=f'style_{i + j}'))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎨 Выберите стиль одежды:",
        reply_markup=reply_markup
    )
    return STYLE


async def get_style(update: Update, context):
    """Показываем кнопки со стилями для выбора"""
    # Делим стили на строки по 3
    keyboard = []
    for i in range(0, len(STYLES), 3):
        row = []
        for j in range(3):
            if i + j < len(STYLES):
                style_text = STYLES[i + j].split('(')[0].strip()
                row.append(InlineKeyboardButton(style_text, callback_data=f'style_{i + j}'))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎨 Выберите ОДИН стиль одежды:",
        reply_markup=reply_markup
    )
    return STYLE


async def get_color(update: Update, context):
    """Показываем кнопки с цветами"""
    # Делим цвета на строки по 4
    keyboard = []
    for i in range(0, len(COLORS), 4):
        row = []
        for j in range(4):
            if i + j < len(COLORS):
                color_text = COLORS[i + j].split(' ')[1]  # Берем только название цвета
                row.append(InlineKeyboardButton(color_text, callback_data=f'color_{i + j}'))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌈 Выберите ОДИН основной цвет:",
        reply_markup=reply_markup
    )
    return COLOR


async def get_photo(update: Update, context):
    user_id = update.message.from_user.id
    photo_file = await update.message.photo[-1].get_file()

    item = user_data_temp.get(user_id, {})
    item['photo_id'] = photo_file.file_id
    item['user_id'] = user_id
    item['username'] = update.message.from_user.username or "Без имени"

    # Сохраняем в JSON
    product_id = add_product(item)

    await update.message.reply_text(f"""
✅ Товар #{product_id} добавлен на модерацию!
📌 {item.get('title')}
💰 {item.get('price')} руб.
🎨 {item.get('style')}

Модератор проверит его в течение 24 часов.
    """)

    # Отправляем админу
    if ADMIN_CHAT_ID:
        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрить", callback_data=f'approve_{product_id}'),
                InlineKeyboardButton("❌ Отклонить", callback_data=f'reject_{product_id}')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📦 Новый товар #{product_id}\nОт: @{item.get('username')}\n\n"
                 f"Название: {item.get('title')}\n"
                 f"Цена: {item.get('price')} руб.\n"
                 f"Стиль: {item.get('style')}\n"
                 f"Цвет: {item.get('color')}\n"
                 f"Описание: {item.get('description')}",
            reply_markup=reply_markup
        )
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=item['photo_id'])

    # Очищаем временные данные
    if user_id in user_data_temp:
        del user_data_temp[user_id]

    return ConversationHandler.END


async def cancel(update: Update, context):
    user_id = update.message.from_user.id
    if user_id in user_data_temp:
        del user_data_temp[user_id]
    await update.message.reply_text('❌ Добавление товара отменено.')
    return ConversationHandler.END


# Обработчики кнопок меню
async def add_item_command(update: Update, context):
    keyboard = [[InlineKeyboardButton("Начать добавление", callback_data='add_item')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📦 Чтобы добавить товар, нажмите кнопку ниже:",
        reply_markup=reply_markup
    )


async def my_items_command(update: Update, context):
    user_id = update.message.from_user.id
    with open('products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_products = [p for p in data['products'] if p.get('user_id') == user_id]

    if not user_products:
        await update.message.reply_text("📭 У вас еще нет добавленных товаров.")
        return

    text = "📋 Ваши товары:\n\n"
    for p in user_products[-5:]:
        status_emoji = "✅" if p['status'] == 'approved' else "⏳" if p['status'] == 'pending' else "❌"
        text += f"{status_emoji} {p['title']} - {p['price']} руб. ({p['status']})\n"

    await update.message.reply_text(text)


async def browse_items_command(update: Update, context):
    with open('products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    approved = [p for p in data['products'] if p['status'] == 'approved']

    if not approved:
        await update.message.reply_text("🛍️ Пока нет товаров в продаже. Будьте первым!")
        return

    text = "🛍️ Последние товары:\n\n"
    for p in approved[-3:]:
        text += f"📌 {p['title']}\n💰 {p['price']} руб.\n🎨 {p['style']}\n\n"

    text += "👉 Полный каталог: https://your-website.com"
    await update.message.reply_text(text)


async def help_command(update: Update, context):
    await update.message.reply_text(
        "ℹ️ *2ndWear FAQ*\n\n"
        "• *Добавить товар* - нажмите '📤 Добавить товар'\n"
        "• *Купить* - смотрите каталог на сайте\n"
        "• *Связаться с продавцом* - нажмите 'Купить' на сайте\n"
        "• *Статус товара* - проверяйте в 'Мои товары'\n\n"
        "Сайт: https://your-website.com",
        parse_mode='Markdown'
    )


async def profile_command(update: Update, context):
    user = update.message.from_user
    with open('products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_products = [p for p in data['products'] if p.get('user_id') == user.id]
    approved = len([p for p in user_products if p['status'] == 'approved'])

    await update.message.reply_text(
        f"👤 *Ваш профиль*\n\n"
        f"Имя: {user.first_name}\n"
        f"Username: @{user.username or 'нет'}\n"
        f"Товаров: {len(user_products)}\n"
        f"Одобрено: {approved}\n"
        f"На модерации: {len(user_products) - approved}",
        parse_mode='Markdown'
    )


# Главная функция
def main():
    # Простая инициализация
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики текстовых команд из меню
    application.add_handler(MessageHandler(filters.Text(["📤 Добавить товар"]), add_item_command))
    application.add_handler(MessageHandler(filters.Text(["📋 Мои товары"]), my_items_command))
    application.add_handler(MessageHandler(filters.Text(["🛍️ Купить"]), browse_items_command))
    application.add_handler(MessageHandler(filters.Text(["ℹ️ Помощь"]), help_command))
    application.add_handler(MessageHandler(filters.Text(["👤 Профиль"]), profile_command))

    # ConversationHandler для добавления товара
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^add_item$')],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
            STYLE: [CallbackQueryHandler(button_handler, pattern='^style_')],
            COLOR: [CallbackQueryHandler(button_handler, pattern='^color_')],
            PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()
