# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def create_user(db: Session, data: schemas.UserCreate):
    user = models.User(username=data.username, telegram_id=data.telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(db: Session, telegram_id: str, username: str | None = None, contact: str | None = None):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if user:
        updated = False
        if username and user.username != username:
            user.username = username
            updated = True
        if contact and user.contact != contact:
            user.contact = contact
            updated = True
        if updated:
            db.commit()
            db.refresh(user)
        return user

    user = models.User(username=username, telegram_id=telegram_id, contact=contact)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


def create_category(db: Session, name: str):
    """Создать или получить категорию"""
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if category:
        return category
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()


def create_product(db: Session, data: schemas.ProductCreate, seller_id: str):
    product = models.Product(
        **data.dict(),
        seller_id=seller_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(
    db: Session,
    search: str = None,
    category_id: int = None,
    section: str = None,
    size: str = None,
    color: str = None,
    style: str = None,
    gender: str = None,
    condition: str = None,
    skip: int = 0,
    limit: int = 100,
):
    """Получить товары с поддержкой фильтрации и пагинации"""
    q = db.query(models.Product)
    
    # Фильтр по поисковой строке
    if search:
        q = q.filter(
            or_(
                models.Product.title.ilike(f"%{search}%"),
                models.Product.description.ilike(f"%{search}%"),
            )
        )
    
    # Фильтры по полям
    if category_id:
        q = q.filter(models.Product.category_id == category_id)
    if section:
        q = q.filter(models.Product.section == section)
    if size:
        q = q.filter(models.Product.size == size)
    if color:
        q = q.filter(models.Product.color == color)
    if style:
        q = q.filter(models.Product.style == style)
    if gender:
        q = q.filter(models.Product.gender == gender)
    if condition:
        q = q.filter(models.Product.condition == condition)
    
    # Сортировка и пагинация
    return q.order_by(models.Product.created_at.desc()).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: str):
    """Получить товар по ID"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


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
