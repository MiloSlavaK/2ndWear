// src/api/client.ts
/**
 * API Client для 2ndWear Backend
 * Замещает Firebase и обеспечивает единое подключение к FastAPI
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Логирование для диагностики
const log = {
    info: (msg: string, data?: any) => {
        console.log(`[API] ${msg}`, data ? data : '');
    },
    error: (msg: string, error?: any) => {
        console.error(`[API ERROR] ${msg}`, error ? error : '');
    },
    request: (method: string, url: string, options?: any) => {
        console.log(`[API REQUEST] ${method} ${url}`, options || '');
    },
    response: (status: number, url: string, data?: any) => {
        console.log(`[API RESPONSE] ${status} ${url}`, data ? `(${typeof data === 'object' ? Object.keys(data).length + ' items' : data})` : '');
    },
};

interface FetchOptions {
    method?: string;
    headers?: Record<string, string>;
    body?: string;
}

async function fetchAPI(endpoint: string, options: FetchOptions = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    log.request(options.method || 'GET', url);
    
    try {
        const response = await fetch(url, {
            method: options.method || "GET",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...(options.body && { body: options.body }),
        });

        log.response(response.status, url);

        if (!response.ok) {
            let error: any = { status: response.status };
            try {
                error = await response.json();
            } catch {
                error.detail = await response.text();
            }
            throw new Error(error.detail || `API Error: ${response.status}`);
        }

        const data = await response.json();
        log.info(`✓ ${endpoint} returned ${Array.isArray(data) ? data.length : 1} items`);
        return data;
    } catch (error) {
        log.error(`${endpoint}`, error);
        throw error;
    }
}

export interface Product {
    id: string;
    title: string;
    description?: string;
    price: number;
    category_id?: number;
    image_url?: string;
    image_key?: string;
    seller_id: string;
    seller_username?: string;
    seller_contact?: string;
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

export async function getProduct(productId: string): Promise<Product> {
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
