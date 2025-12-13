# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    telegram_id = Column(String, nullable=True)

    products = relationship("Product", back_populates="seller")
    messages = relationship("Message", back_populates="sender")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship("User", back_populates="products")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="messages")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(String, default="initiated")
    created_at = Column(DateTime, default=datetime.utcnow)
