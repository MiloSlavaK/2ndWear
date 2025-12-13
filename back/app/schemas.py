# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    telegram_id: Optional[str] = None


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    title: str
    description: Optional[str]
    price: float
    category: Optional[str]
    image_url: Optional[str]


class Product(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    category: Optional[str]
    image_url: Optional[str]
    seller_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    product_id: int
    sender_id: int
    text: str


class Message(BaseModel):
    id: int
    text: str
    sender_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    buyer_id: int
    product_id: int


class Order(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
