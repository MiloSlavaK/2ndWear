# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    telegram_id: Optional[str] = None


class User(BaseModel):
    id: str
    username: str
    telegram_id: Optional[str] = None

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    # Новые поля для фильтрации
    size: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None
    gender: Optional[str] = None
    condition: Optional[str] = None
    section: str = "market"  # market, swop, charity


class Product(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: float
    category_id: Optional[int]
    image_url: Optional[str]
    seller_id: str
    seller_username: Optional[str] = None  # Username продавца для покупателей
    # Поля фильтрации
    size: Optional[str]
    color: Optional[str]
    style: Optional[str]
    gender: Optional[str]
    condition: Optional[str]
    section: str
    created_at: datetime

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    product_id: str
    sender_id: str
    text: str


class Message(BaseModel):
    id: str
    text: str
    sender_id: str
    product_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    buyer_id: str
    product_id: str


class Order(BaseModel):
    id: str
    buyer_id: str
    product_id: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
