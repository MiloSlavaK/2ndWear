// src/api/client.ts
/**
 * API Client для 2ndWear Backend
 * Замещает Firebase и обеспечивает единое подключение к FastAPI
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface FetchOptions {
    method?: string;
    headers?: Record<string, string>;
    body?: string;
}

async function fetchAPI(endpoint: string, options: FetchOptions = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
        method: options.method || "GET",
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
        ...(options.body && { body: options.body }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
}

export interface Product {
    id: number;
    title: string;
    description?: string;
    price: number;
    category_id?: number;
    image_url?: string;
    seller_id: number;
    size?: string;
    color?: string;
    style?: string;
    gender?: string;
    condition?: string;
    section: "market" | "swop" | "charity";
    created_at: string;
}

export interface Category {
    id: number;
    name: string;
}

export interface Message {
    id: number;
    text: string;
    sender_id: number;
    product_id: number;
    created_at: string;
}

export interface Order {
    id: number;
    buyer_id: number;
    product_id: number;
    status: string;
    created_at: string;
}

// ============= PRODUCTS =============
export async function getProducts(filters?: {
    search?: string;
    section?: string;
    category_id?: number;
    size?: string;
    color?: string;
    style?: string;
    gender?: string;
    condition?: string;
    skip?: number;
    limit?: number;
}): Promise<Product[]> {
    const params = new URLSearchParams();
    
    if (filters) {
        if (filters.search) params.append("search", filters.search);
        if (filters.section) params.append("section", filters.section);
        if (filters.category_id) params.append("category_id", String(filters.category_id));
        if (filters.size) params.append("size", filters.size);
        if (filters.color) params.append("color", filters.color);
        if (filters.style) params.append("style", filters.style);
        if (filters.gender) params.append("gender", filters.gender);
        if (filters.condition) params.append("condition", filters.condition);
        if (filters.skip !== undefined) params.append("skip", String(filters.skip));
        if (filters.limit !== undefined) params.append("limit", String(filters.limit));
    }

    const endpoint = params.toString() ? `/products?${params.toString()}` : "/products";
    return fetchAPI(endpoint);
}

export async function getProduct(productId: number): Promise<Product> {
    return fetchAPI(`/products/${productId}`);
}

export async function createProduct(product: Omit<Product, "id" | "created_at" | "seller_id">, sellerId: number): Promise<Product> {
    return fetchAPI("/products/", {
        method: "POST",
        body: JSON.stringify(product),
        headers: { "seller_id": String(sellerId) },
    });
}

// ============= CATEGORIES =============
export async function getCategories(): Promise<Category[]> {
    return fetchAPI("/categories");
}

export async function getCategory(categoryId: number): Promise<Category> {
    return fetchAPI(`/categories/${categoryId}`);
}

export async function createCategory(name: string): Promise<Category> {
    return fetchAPI("/categories", {
        method: "POST",
        body: JSON.stringify({ name }),
    });
}

// ============= MESSAGES =============
export async function getMessages(productId: number): Promise<Message[]> {
    return fetchAPI(`/messages/product/${productId}`);
}

export async function sendMessage(productId: number, senderId: number, text: string): Promise<Message> {
    return fetchAPI("/messages", {
        method: "POST",
        body: JSON.stringify({
            product_id: productId,
            sender_id: senderId,
            text,
        }),
    });
}

// ============= ORDERS =============
export async function createOrder(buyerId: number, productId: number): Promise<Order> {
    return fetchAPI("/orders", {
        method: "POST",
        body: JSON.stringify({
            buyer_id: buyerId,
            product_id: productId,
        }),
    });
}

export async function getOrder(orderId: number): Promise<Order> {
    return fetchAPI(`/orders/${orderId}`);
}

export async function getOrderSummary(orderId: number) {
    return fetchAPI(`/orders/${orderId}/summary`);
}

// ============= HEALTH CHECK =============
export async function checkHealth() {
    try {
        return await fetchAPI("/health");
    } catch (error) {
        console.error("Health check failed:", error);
        return null;
    }
}

export default {
    getProducts,
    getProduct,
    createProduct,
    getCategories,
    getCategory,
    createCategory,
    getMessages,
    sendMessage,
    createOrder,
    getOrder,
    getOrderSummary,
    checkHealth,
};
