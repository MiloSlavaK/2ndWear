# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, data: schemas.UserCreate):
    user = models.User(username=data.username, telegram_id=data.telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(db: Session, telegram_id: str):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if user:
        return user

    user = models.User(username=f"user_{telegram_id}", telegram_id=telegram_id)
    db.add(user)
    db.commit()
    return user


def create_product(db: Session, data: schemas.ProductCreate, seller_id: int):
    product = models.Product(**data.dict(), seller_id=seller_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, search: str = None, category: str = None):
    q = db.query(models.Product)
    if search:
        q = q.filter(models.Product.title.ilike(f"%{search}%"))
    if category:
        q = q.filter(models.Product.category == category)
    return q.order_by(models.Product.created_at.desc()).all()


def create_message(db: Session, data: schemas.MessageCreate):
    msg = models.Message(**data.dict())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def create_order(db: Session, data: schemas.OrderCreate):
    order = models.Order(**data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
