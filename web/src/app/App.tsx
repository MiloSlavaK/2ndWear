import { useState, useEffect } from "react";
import { ProductCard } from "./components/ProductCard";
import { FilterBar } from "./components/FilterBar";
import { db } from "../firebase"; // Импортируйте ваш firebase config
import { collection, getDocs } from "firebase/firestore";
import headerImage from "../assets/header.png";

interface Product {
    id: string; // Изменили на string для Firestore ID
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

export default function App() {
    const [activeSection, setActiveSection] = useState<"market" | "swop" | "charity">("market");
    const [selectedStyle, setSelectedStyle] = useState("Все");
    const [selectedColor, setSelectedColor] = useState("Все");
    const [selectedSize, setSelectedSize] = useState("Все");
    const [selectedGender, setSelectedGender] = useState("Все");
    const [selectedClothingCategory, setSelectedClothingCategory] = useState("Все");
    const [selectedCondition, setSelectedCondition] = useState("Все");

    // Новые состояния для Firebase
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Загрузка товаров из Firebase
    useEffect(() => {
        async function loadProducts() {
            try {
                setLoading(true);
                setError(null);

                console.log("Начинаю загрузку товаров из Firebase...");
                const querySnapshot = await getDocs(collection(db, "products"));
                console.log(`Получено ${querySnapshot.size} товаров из Firebase`);

                const productsList: Product[] = [];

                querySnapshot.forEach((doc) => {
                    const data = doc.data();
                    console.log(`Товар ${doc.id}:`, data);

                    // Маппинг полей из Firebase в нашу структуру
                    productsList.push({
                        id: doc.id, // Firestore ID
                        name: data.name || data.название || "Без названия",
                        price: Number(data.price) || Number(data.цена) || 0,
                        size: data.size || data.размер || "",
                        color: data.color || data.цвет || "",
                        style: data.style || data.стиль || "👖 Casual (Повседневный)",
                        gender: data.gender || data.пол || "Унисекс",
                        condition: data.condition || data.состояние || "Хорошее",
                        clothingCategory: data.clothingCategory || data.category || data.категория || "Одежда",
                        image: data.image || data.imageUrl || data.photo || "https://images.unsplash.com/photo-1558769132-cb1adedebc1a?w=400",
                        telegramLink: data.telegramLink || data.telegram || "https://t.me/your2ndWearbot",
                        section: (data.section || data.раздел || "market") as "market" | "swop" | "charity"
                    });
                });

                setProducts(productsList);
                console.log(`Загружено ${productsList.length} товаров`);

            } catch (error) {
                console.error("Ошибка загрузки товаров:", error);
                setError("Не удалось загрузить товары. Проверьте подключение к базе данных.");
            } finally {
                setLoading(false);
            }
        }

        loadProducts();
    }, []);

    // Фильтрация товаров
    const filteredProducts = products.filter((product) => {
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
                {/* Отладочная информация */}
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-700">
                        🔗 Подключено к Firebase | Товаров в базе: {products.length} |
                        Показано: {filteredProducts.length} |
                        Раздел: {activeSection === "market" ? "Маркет" : activeSection === "swop" ? "Обмен" : "Бесплатно"}
                    </p>
                </div>

                {/* Section Navigation */}
                <div className="mb-8">
                    <div className="flex gap-3 justify-center">
                        <button
                            onClick={() => setActiveSection("market")}
                            className={`px-6 py-2 rounded-lg transition-all ${activeSection === "market"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-card text-card-foreground border border-border hover:border-primary"
                                }`}
                        >
                            Маркет
                        </button>
                        <button
                            onClick={() => setActiveSection("swop")}
                            className={`px-6 py-2 rounded-lg transition-all ${activeSection === "swop"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-card text-card-foreground border border-border hover:border-primary"
                                }`}
                        >
                            Обмен
                        </button>
                        <button
                            onClick={() => setActiveSection("charity")}
                            className={`px-6 py-2 rounded-lg transition-all ${activeSection === "charity"
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
                        Найдено товаров: {loading ? "..." : filteredProducts.length}
                    </p>
                </div>

                {error ? (
                    <div className="text-center py-12 bg-red-50 rounded-lg">
                        <p className="text-red-600 font-medium">⚠️ {error}</p>
                        <p className="text-red-500 text-sm mt-2">
                            Проверьте: 1) Подключение к интернету 2) Настройки Firebase 3) Правила доступа к базе
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
                        >
                            Попробовать снова
                        </button>
                    </div>
                ) : loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
                        <p className="mt-4 text-muted-foreground">Загружаем товары из базы данных...</p>
                        <p className="text-sm text-gray-500">Подключение к Firebase...</p>
                    </div>
                ) : filteredProducts.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-muted-foreground">
                            {products.length === 0
                                ? "В базе данных пока нет товаров. Добавьте первый товар через Firebase Console или Telegram бот."
                                : "По вашим фильтрам ничего не найдено. Попробуйте изменить параметры поиска."}
                        </p>
                        {products.length === 0 && (
                            <div className="mt-6 p-4 bg-yellow-50 rounded-lg max-w-md mx-auto">
                                <p className="text-sm text-yellow-700">
                                    💡 Чтобы добавить товар вручную:
                                </p>
                                <ol className="text-sm text-yellow-600 mt-2 text-left list-decimal ml-5">
                                    <li>Откройте Firebase Console</li>
                                    <li>Зайдите в Firestore Database</li>
                                    <li>Нажмите "+ Start collection" → "products"</li>
                                    <li>Добавьте поля: name, price, section, imageUrl</li>
                                </ol>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {filteredProducts.map((product) => (
                            <ProductCard key={product.id} product={product} />
                        ))}
                    </div>
                )}

                {/* Информация о загрузке */}
                {!loading && !error && (
                    <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                        <p className="text-sm text-gray-500">
                            Данные загружены из Firebase. Товаров в базе: {products.length}
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                        >
                            Обновить данные
                        </button>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="bg-card border-t border-border mt-12">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <div className="text-center text-muted-foreground">
                        <p>© 2025 2ndWear. Качественный секонд-хенд онлайн</p>
                        <p className="mt-2">Покупка через Telegram бот</p>
                        <p className="mt-1 text-sm">Powered by Firebase 🔥 | Товаров в базе: {products.length}</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}