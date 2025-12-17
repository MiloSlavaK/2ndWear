import { useState } from "react";
import { ProductCard } from "./components/ProductCard";
import { FilterBar } from "./components/FilterBar";
import headerImage from "figma:asset/57cbd9a32fb3228e2eca14d18055009578e97e93.png";

interface Product {
  id: number;
  name: string;
  price: number;
  size: string;
  color: string;
  style: string;
  gender: string;
  condition: string;
  clothingCategory: string;
  image: string;
  telegramLink: string;
  section: "market" | "swop" | "charity";
}

const mockProducts: Product[] = [
  {
    id: 1,
    name: "Винтажная джинсовая куртка",
    price: 2500,
    size: "M",
    color: "Синий",
    style: "📻 Vintage (Винтаж)",
    gender: "Мужская",
    condition: "Как новое",
    clothingCategory: "Верхняя одежда",
    image: "https://images.unsplash.com/photo-1760533091973-1262bf57d244?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWNvbmRoYW5kJTIwamFja2V0fGVufDF8fHx8MTc2NTcwNTYxN3ww&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "market",
  },
  {
    id: 2,
    name: "Летнее платье с принтом",
    price: 1800,
    size: "S",
    color: "Зеленый",
    style: "🏡 Cottagecore (Деревенский стиль)",
    gender: "Женская",
    condition: "С биркой",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1678935908871-a72d8380baaa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwZHJlc3N8ZW58MXx8fHwxNzY1NzA1NjE3fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "market",
  },
  {
    id: 3,
    name: "Оверсайз свитер",
    price: 1500,
    size: "L",
    color: "Коричневый",
    style: "🎵 Grunge (Гранж)",
    gender: "Женская",
    condition: "Новое",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1765603726152-d99ea17007f9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwc3dlYXRlcnxlbnwxfHx8fDE3NjU3MDU2MTh8MA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "swop",
  },
  {
    id: 4,
    name: "Классические джинсы",
    price: 2000,
    size: "M",
    color: "Синий",
    style: "👖 Casual (Повседневный)",
    gender: "Мужская",
    condition: "Как новое",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1615420733239-070fc4b95914?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwamVhbnN8ZW58MXx8fHwxNzY1NzA1NjE4fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "market",
  },
  {
    id: 5,
    name: "Рубашка в клетку",
    price: 1200,
    size: "L",
    color: "Красный",
    style: "📚 Dark Academia (Темная академия)",
    gender: "Мужская",
    condition: "Имеются повреждения",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1594201638839-e36ddd34822d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwc2hpcnR8ZW58MXx8fHwxNzY1NzA1NjE4fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "swop",
  },
  {
    id: 6,
    name: "Кожаная куртка",
    price: 4500,
    size: "M",
    color: "Черный",
    style: "⚫ Minimalism (Минимализм)",
    gender: "Женская",
    condition: "Новое",
    clothingCategory: "Верхняя одежда",
    image: "https://images.unsplash.com/photo-1614990354198-b06764dcb13c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwY2xvdGhpbmd8ZW58MXx8fHwxNzY1Njk3ODg0fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "market",
  },
  {
    id: 7,
    name: "Белая футболка",
    price: 800,
    size: "S",
    color: "Белый",
    style: "✨ Clean (Чистый стиль)",
    gender: "Детская",
    condition: "С биркой",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1614990354198-b06764dcb13c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwY2xvdGhpbmd8ZW58MXx8fHwxNzY1Njk3ODg0fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "charity",
  },
  {
    id: 8,
    name: "Вельветовые брюки",
    price: 2200,
    size: "XL",
    color: "Коричневый",
    style: "📻 Vintage (Винтаж)",
    gender: "Женская",
    condition: "Как новое",
    clothingCategory: "Одежда",
    image: "https://images.unsplash.com/photo-1760533091973-1262bf57d244?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWNvbmRoYW5kJTIwamFja2V0fGVufDF8fHx8MTc2NTcwNTYxN3ww&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "charity",
  },
  {
    id: 9,
    name: "Спортивная куртка",
    price: 1900,
    size: "M",
    color: "Черный",
    style: "👖 Casual (Повседневный)",
    gender: "Мужская",
    condition: "Новое",
    clothingCategory: "Верхняя одежда",
    image: "https://images.unsplash.com/photo-1760533091973-1262bf57d244?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWNvbmRoYW5kJTIwamFja2V0fGVufDF8fHx8MTc2NTcwNTYxN3ww&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "swop",
  },
  {
    id: 10,
    name: "Теплое пальто",
    price: 3500,
    size: "L",
    color: "Бежевый",
    style: "⚫ Minimalism (Минимализм)",
    gender: "Женская",
    condition: "С биркой",
    clothingCategory: "Верхняя одежда",
    image: "https://images.unsplash.com/photo-1614990354198-b06764dcb13c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aW50YWdlJTIwY2xvdGhpbmd8ZW58MXx8fHwxNzY1Njk3ODg0fDA&ixlib=rb-4.1.0&q=80&w=1080",
    telegramLink: "https://t.me/your2ndWearbot",
    section: "charity",
  },
];

export default function App() {
  const [activeSection, setActiveSection] = useState<"market" | "swop" | "charity">("market");
  const [selectedStyle, setSelectedStyle] = useState("Все");
  const [selectedColor, setSelectedColor] = useState("Все");
  const [selectedSize, setSelectedSize] = useState("Все");
  const [selectedGender, setSelectedGender] = useState("Все");
  const [selectedClothingCategory, setSelectedClothingCategory] = useState("Все");
  const [selectedCondition, setSelectedCondition] = useState("Все");

  const filteredProducts = mockProducts.filter((product) => {
    const sectionMatch = product.section === activeSection;
    const styleMatch = selectedStyle === "Все" || product.style === selectedStyle;
    const colorMatch = selectedColor === "Все" || product.color === selectedColor;
    const sizeMatch = selectedSize === "Все" || product.size === selectedSize;
    const genderMatch = selectedGender === "Все" || product.gender === selectedGender;
    const clothingCategoryMatch = selectedClothingCategory === "Все" || product.clothingCategory === selectedClothingCategory;
    const conditionMatch = selectedCondition === "Все" || product.condition === selectedCondition;
    return sectionMatch && styleMatch && colorMatch && sizeMatch && genderMatch && clothingCategoryMatch && conditionMatch;
  });

  const handleReset = () => {
    setSelectedStyle("Все");
    setSelectedColor("Все");
    setSelectedSize("Все");
    setSelectedGender("Все");
    setSelectedClothingCategory("Все");
    setSelectedCondition("Все");
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="shadow-sm">
        <div className="w-full">
          <img 
            src={headerImage} 
            alt="2ndWear" 
            className="w-full h-auto object-cover"
          />
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Section Navigation - Centered */}
        <div className="mb-8">
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => setActiveSection("market")}
              className={`px-6 py-2 rounded-lg transition-all ${
                activeSection === "market"
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-card-foreground border border-border hover:border-primary"
              }`}
            >
              Маркет
            </button>
            <button
              onClick={() => setActiveSection("swop")}
              className={`px-6 py-2 rounded-lg transition-all ${
                activeSection === "swop"
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-card-foreground border border-border hover:border-primary"
              }`}
            >
              Обмен
            </button>
            <button
              onClick={() => setActiveSection("charity")}
              className={`px-6 py-2 rounded-lg transition-all ${
                activeSection === "charity"
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-card-foreground border border-border hover:border-primary"
              }`}
            >
              Бесплатно
            </button>
          </div>
        </div>

        {/* Filters */}
        <FilterBar
          selectedStyle={selectedStyle}
          selectedColor={selectedColor}
          selectedSize={selectedSize}
          selectedGender={selectedGender}
          selectedClothingCategory={selectedClothingCategory}
          selectedCondition={selectedCondition}
          onStyleChange={setSelectedStyle}
          onColorChange={setSelectedColor}
          onSizeChange={setSelectedSize}
          onGenderChange={setSelectedGender}
          onCategoryChange={setSelectedClothingCategory}
          onConditionChange={setSelectedCondition}
          onReset={handleReset}
        />

        {/* Products Grid */}
        <div className="mb-4">
          <p className="text-muted-foreground">
            Найдено товаров: {filteredProducts.length}
          </p>
        </div>

        {filteredProducts.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">
              По вашим фильтрам ничего не найдено. Попробуйте изменить параметры поиска.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-card border-t border-border mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="text-center text-muted-foreground">
            <p>© 2025 2ndWear. Качественный секонд-хенд онлайн</p>
            <p className="mt-2">Покупка через Telegram бот</p>
          </div>
        </div>
      </footer>
    </div>
  );
}