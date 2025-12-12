import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', 0))

# Временное хранилище
user_data_temp = {}

# Фиксированные стили для выбора
STYLES = [
    "🏃 Sport (Спортивный)",
    "👔 Classic (Классический)",
    "📻 Vintage (Винтаж)",
    "🧜‍♀️ Mermaidcore (Русалочий стиль)",
    "💼 Officecore (Офисный стиль)",
    "🩰 Balletcore (Балетный стиль)",
    "🏡 Cottagecore (Деревенский стиль)",
    "🍄 Goblin core (Гоблинский стиль)",
    "🧚 Fairycore (Феечный стиль)",
    "🦇 Goth (Готический)",
    "🌸 Kawaii (Кавайный)",
    "📱 Y2K (Стиль 2000-х)",
    "🎸 Emo (Эмо)",
    "🎵 Grunge (Гранж)",
    "⚫ Minimalism (Минимализм)",
    "🎨 Indie Kid (Инди)",
    "📚 Dark Academia (Темная академия)",
    "☕ Light Academia (Светлая академия)",
    "⚡ Punk (Панк)",
    "🌿 Boho (Бохо)",
    "✨ Clean (Чистый стиль)",
    "🛹 Streetwear (Уличный стиль)",
    "👗 Model off Duty (Стиль модели)",
    "👖 Casual (Повседневный)",
    "🤵 Smart Casual (Умный кэжуал)",
    "🚀 Futuristic (Футуристический)",
    "🌿 Eco (Эко-стиль)"
]

# Фиксированные цвета
COLORS = [
    "⚫ Черный",
    "⚪ Белый",
    "🔵 Синий",
    "🔴 Красный",
    "🟢 Зеленый",
    "🟡 Желтый",
    "🟣 Фиолетовый",
    "🟠 Оранжевый",
    "🟤 Коричневый",
    "⚪ Серый",
    "🩷 Розовый",
    "🧵 Бежевый",
    "🌫️ Голубой",
    "🍁 Бордовый",
    "🦢 Мятный",
    "🌙 Лавандовый",
    "🍑 Персиковый",
    "🌊 Бирюзовый",
    "🍫 Шоколадный",
    "🌅 Омбре"
]

# Категории для фильтров на сайте
STYLE_CATEGORIES = {
    "Спортивные": ["Sport", "Streetwear"],
    "Классические": ["Classic", "Officecore", "Clean", "Smart Casual"],
    "Романтичные": ["Balletcore", "Cottagecore", "Fairycore", "Light Academia"],
    "Альтернативные": ["Goth", "Emo", "Grunge", "Punk", "Dark Academia"],
    "Молодежные": ["Kawaii", "Y2K", "Indie Kid", "Model off Duty"],
    "Природные": ["Mermaidcore", "Goblin core", "Boho", "Eco", "Vintage"],
    "Минимализм": ["Minimalism", "Clean"],
    "Футуристичные": ["Futuristic"]
}
