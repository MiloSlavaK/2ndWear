import { SlidersHorizontal, X } from "lucide-react";
import { useState } from "react";

interface FilterBarProps {
  selectedStyle: string;
  selectedColor: string;
  selectedSize: string;
  selectedGender: string;
  selectedClothingCategory: string;
  selectedCondition: string;
  onStyleChange: (style: string) => void;
  onColorChange: (color: string) => void;
  onSizeChange: (size: string) => void;
  onGenderChange: (gender: string) => void;
  onCategoryChange: (category: string) => void;
  onConditionChange: (condition: string) => void;
  onReset: () => void;
}

export function FilterBar({
  selectedStyle,
  selectedColor,
  selectedSize,
  selectedGender,
  selectedClothingCategory,
  selectedCondition,
  onStyleChange,
  onColorChange,
  onSizeChange,
  onGenderChange,
  onCategoryChange,
  onConditionChange,
  onReset,
}: FilterBarProps) {
  const [isOpen, setIsOpen] = useState(false);

  const styles = [
    "Все",
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
    "🌿 Other (Другое)"
  ];
  const colors = ["Все", "Черный", "Белый", "Синий", "Зеленый", "Красный", "Коричневый"];
  const sizes = ["Все", "XS", "S", "M", "L", "XL"];
  const genders = ["Все", "Мужская", "Женская", "Детская"];
  const clothingCategories = ["Все", "Верхняя одежда", "Одежда", "Обувь", "Аксессуары"];
  const conditions = ["Все", "С биркой", "Новое", "Как новое", "Имеются повреждения"];

  const hasActiveFilters = selectedStyle !== "Все" || selectedColor !== "Все" || selectedSize !== "Все" || selectedGender !== "Все" || selectedClothingCategory !== "Все" || selectedCondition !== "Все";

  return (
    <div className="bg-card border border-border rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="w-5 h-5 text-primary" />
          <h3>Фильтры</h3>
        </div>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="lg:hidden px-3 py-1 bg-secondary text-secondary-foreground rounded"
        >
          {isOpen ? "Скрыть" : "Показать"}
        </button>
      </div>

      <div className={`${isOpen ? "block" : "hidden"} lg:block`}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block mb-2 text-muted-foreground">Стиль</label>
            <select
              value={selectedStyle}
              onChange={(e) => onStyleChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {styles.map((style) => (
                <option key={style} value={style}>
                  {style}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 text-muted-foreground">Цвет</label>
            <select
              value={selectedColor}
              onChange={(e) => onColorChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {colors.map((color) => (
                <option key={color} value={color}>
                  {color}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 text-muted-foreground">Размер</label>
            <select
              value={selectedSize}
              onChange={(e) => onSizeChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {sizes.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 text-muted-foreground">Пол</label>
            <select
              value={selectedGender}
              onChange={(e) => onGenderChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {genders.map((gender) => (
                <option key={gender} value={gender}>
                  {gender}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 text-muted-foreground">Категория одежды</label>
            <select
              value={selectedClothingCategory}
              onChange={(e) => onCategoryChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {clothingCategories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 text-muted-foreground">Состояние</label>
            <select
              value={selectedCondition}
              onChange={(e) => onConditionChange(e.target.value)}
              className="w-full px-3 py-2 bg-input-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {conditions.map((condition) => (
                <option key={condition} value={condition}>
                  {condition}
                </option>
              ))}
            </select>
          </div>
        </div>

        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="mt-4 flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-4 h-4" />
            Сбросить фильтры
          </button>
        )}
      </div>
    </div>
  );
}