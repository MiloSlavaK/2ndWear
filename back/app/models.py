# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import uuid


def generate_uuid():
    """Генерирует UUID как строку без дефисов (32 символа)"""
    return uuid.uuid4().hex


class User(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, index=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=True)
    telegram_id = Column(String, nullable=True)
    contact = Column(String, nullable=True)  # телефон или иной контакт

    products = relationship("Product", back_populates="seller")
    messages = relationship("Message", back_populates="sender")


class Category(Base):
    """Категория одежды (Одежда, Обувь, Аксессуары и т.д.)"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Одежда, Обувь, Аксессуары
    
    products = relationship("Product", back_populates="category_obj")


class Product(Base):
    __tablename__ = "products"

    id = Column(String(32), primary_key=True, index=True, default=generate_uuid)
    seller_id = Column(String(32), ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # FK на Category
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    image_key = Column(String, nullable=True)
    seller_username = Column(String, nullable=True)
    seller_contact = Column(String, nullable=True)

    # Новые поля для фильтрации (из требований фронтенда)
    size = Column(String, nullable=True)  # XS, S, M, L, XL
    color = Column(String, nullable=True)  # Черный, Белый, Синий и т.д.
    style = Column(String, nullable=True)  # Casual, Formal, Sport и т.д.
    gender = Column(String, nullable=True)  # Мужской, Женский, Унисекс
    condition = Column(String, nullable=True)  # Отличное, Хорошее, Нормальное и т.д.
    section = Column(String, default="market")  # market, swop, charity

    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship("User", back_populates="products")
    category_obj = relationship("Category", back_populates="products")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(32), primary_key=True, default=generate_uuid)
    product_id = Column(String(32), ForeignKey("products.id"))
    sender_id = Column(String(32), ForeignKey("users.id"))

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="messages")


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(32), primary_key=True, default=generate_uuid)
    buyer_id = Column(String(32), ForeignKey("users.id"))
    product_id = Column(String(32), ForeignKey("products.id"))
    status = Column(String, default="initiated")  # initiated, confirmed, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
