import json
import os
from datetime import datetime

DATA_FILE = 'products.json'


def init_database():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"products": []}, f, ensure_ascii=False, indent=2)


def add_product(product_data):
    init_database()

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    product = {
        "id": len(data["products"]) + 1,
        "title": product_data.get("title", ""),
        "price": product_data.get("price", 0),
        "description": product_data.get("description", ""),
        "style": product_data.get("style", ""),
        "color": product_data.get("color", ""),
        "photo_id": product_data.get("photo_id", ""),
        "user_id": product_data.get("user_id", ""),
        "username": product_data.get("username", ""),
        "status": "pending",  # pending, approved, rejected
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data["products"].append(product)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return product["id"]


def get_approved_products():
    init_database()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [p for p in data["products"] if p["status"] == "approved"]


def get_styles():
    products = get_approved_products()
    styles = list(set(p["style"].lower() for p in products if p["style"]))
    return sorted(styles)


def get_colors():
    products = get_approved_products()
    colors = list(set(p["color"].lower() for p in products if p["color"]))
    return sorted(colors)