import { useState, useEffect } from "react";
import { ProductCard } from "./components/ProductCard";
import { FilterBar } from "./components/FilterBar";
import { getProducts } from "../api/client";
import type { Product } from "../api/client";
import headerImage from "../assets/header.png";

export default function App() {
    const [activeSection, setActiveSection] = useState<"market" | "swop" | "charity">("market");
    const [selectedStyle, setSelectedStyle] = useState("Все");
    const [selectedColor, setSelectedColor] = useState("Все");
    const [selectedSize, setSelectedSize] = useState("Все");
    const [selectedGender, setSelectedGender] = useState("Все");
    const [selectedClothingCategory, setSelectedClothingCategory] = useState("Все");
    const [selectedCondition, setSelectedCondition] = useState("Все");

    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Загрузка товаров с бэкенда
    useEffect(() => {
        async function loadProducts() {
            try {
                setLoading(true);
                setError(null);

                console.log("Loading products from FastAPI...");
                // Передаём фильтры на сервер для оптимизации
                const loadedProducts = await getProducts({
                    section: activeSection,
                    ...(selectedStyle !== "Все" && { style: selectedStyle }),
                    ...(selectedColor !== "Все" && { color: selectedColor }),
                    ...(selectedSize !== "Все" && { size: selectedSize }),
                    ...(selectedGender !== "Все" && { gender: selectedGender }),
                    ...(selectedCondition !== "Все" && { condition: selectedCondition }),
                });

                console.log(`Loaded ${loadedProducts.length} products from backend`);
                setProducts(loadedProducts);
            } catch (error) {
                console.error("Error loading products:", error);
                setError("Failed to load products. Please check your connection.");
            } finally {
                setLoading(false);
            }
        }

        loadProducts();
    }, [activeSection, selectedStyle, selectedColor, selectedSize, selectedGender, selectedCondition]);

    // Локальная фильтрация для полей, которые могут не быть на сервере
    const filteredProducts = products.filter((product) => {
        const styleMatch = selectedStyle === "Все" || product.style === selectedStyle;
        const colorMatch = selectedColor === "Все" || product.color === selectedColor;
        const sizeMatch = selectedSize === "Все" || product.size === selectedSize;
        const genderMatch = selectedGender === "Все" || product.gender === selectedGender;
        const categoryMatch = selectedClothingCategory === "Все" || product.title.includes(selectedClothingCategory);
        const conditionMatch = selectedCondition === "Все" || product.condition === selectedCondition;

        return styleMatch && colorMatch && sizeMatch && genderMatch && categoryMatch && conditionMatch;
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
                {/* Debug Info */}
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-700">
                        🔗 Connected to FastAPI | Total: {products.length} | Shown: {filteredProducts.length} |
                        Section: {activeSection === "market" ? "Marketplace" : activeSection === "swop" ? "Swap" : "Free"}
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
                            Marketplace
                        </button>
                        <button
                            onClick={() => setActiveSection("swop")}
                            className={`px-6 py-2 rounded-lg transition-all ${activeSection === "swop"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-card text-card-foreground border border-border hover:border-primary"
                                }`}
                        >
                            Swap
                        </button>
                        <button
                            onClick={() => setActiveSection("charity")}
                            className={`px-6 py-2 rounded-lg transition-all ${activeSection === "charity"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-card text-card-foreground border border-border hover:border-primary"
                                }`}
                        >
                            Free
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
                        Found: {loading ? "..." : filteredProducts.length}
                    </p>
                </div>

                {error ? (
                    <div className="text-center py-12 bg-red-50 rounded-lg">
                        <p className="text-red-600 font-medium">⚠️ {error}</p>
                        <p className="text-red-500 text-sm mt-2">
                            Make sure: 1) Internet is working 2) FastAPI backend is running on http://localhost:8000
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
                        >
                            Retry
                        </button>
                    </div>
                ) : loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
                        <p className="mt-4 text-muted-foreground">Loading products...</p>
                        <p className="text-sm text-gray-500">Connected to FastAPI Backend</p>
                    </div>
                ) : filteredProducts.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-muted-foreground">
                            {products.length === 0
                                ? "No products available. Add your first item via Telegram bot (@your2ndWearbot)."
                                : "No products match your filters. Try changing them."}
                        </p>
                        {products.length === 0 && (
                            <div className="mt-6 p-4 bg-yellow-50 rounded-lg max-w-md mx-auto">
                                <p className="text-sm text-yellow-700">
                                    💡 To add a product:
                                </p>
                                <ol className="text-sm text-yellow-600 mt-2 text-left list-decimal ml-5">
                                    <li>Open Telegram</li>
                                    <li>Find @2ndWearBot</li>
                                    <li>Press "Add Product" button</li>
                                    <li>Fill in all product details</li>
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

                {/* Footer Info */}
                {!loading && !error && (
                    <div className="mt-8 pt-6 border-t border-gray-200 text-center">
                        <p className="text-sm text-gray-500">
                            Data from 2ndWear Backend. Total products: {products.length}
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                        >
                            Refresh
                        </button>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="bg-card border-t border-border mt-12">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <div className="text-center text-muted-foreground">
                        <p>© 2025 2ndWear. Quality secondhand fashion online</p>
                        <p className="mt-2">Shopping via Telegram Bot</p>
                        <p className="mt-1 text-sm">Powered by FastAPI ⚡ | {products.length} products available</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}