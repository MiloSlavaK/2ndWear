#!/usr/bin/env python3
"""
Скрипт миграции БД: Integer ID → UUID

ВНИМАНИЕ: Этот скрипт пересоздаст все таблицы с нуля!
Все существующие данные будут потеряны.

Для production используйте Alembic для безопасной миграции.

Использование:
    python migrate_to_uuid.py
"""
import sys
import os

# Добавляем путь к app для импорта
sys.path.insert(0, os.path.dirname(__file__))

from app.db import Base, engine
from app.models import User, Product, Category, Message, Order


def migrate():
    print("⚠️  ВНИМАНИЕ: Этот скрипт удалит ВСЕ существующие данные!")
    print("Продолжить? (yes/no): ", end="")
    
    confirm = input().strip().lower()
    if confirm != "yes":
        print("❌ Миграция отменена.")
        return
    
    print("\n🗑️  Удаление старых таблиц...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Старые таблицы удалены")
    
    print("\n🔨 Создание новых таблиц с UUID...")
    Base.metadata.create_all(bind=engine)
    print("✅ Новые таблицы созданы")
    
    print("\n✨ Миграция завершена!")
    print("\nСтруктура таблиц:")
    print("  - users: id (String(32) UUID)")
    print("  - products: id (String(32) UUID), seller_id (String(32))")
    print("  - messages: id (String(32) UUID), product_id, sender_id")
    print("  - orders: id (String(32) UUID), buyer_id, product_id")
    print("  - categories: id (Integer) - не изменилась")


if __name__ == "__main__":
    migrate()
