# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import crud, schemas, models
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Product)
def create_product(
    data: schemas.ProductCreate,
    seller_id: str,
    db: Session = Depends(get_db)
):
    """Создать новый товар (из Telegram-бота или фронтенда)"""
    logger.info("Creating product: seller_id=%s, title=%s", seller_id, data.title)
    return crud.create_product(db, data, seller_id)


@router.get("/", response_model=list[schemas.Product])
def list_products(
    search: str | None = None,
    category_id: int | None = None,
    section: str | None = None,
    size: str | None = None,
    color: str | None = None,
    style: str | None = None,
    gender: str | None = None,
    condition: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получить список товаров с поддержкой фильтрации.
    
    Параметры:
    - search: Поиск по названию или описанию
    - section: market, swop, charity
    - size, color, style, gender, condition: Фильтры
    - skip, limit: Пагинация
    """
    logger.info(
        "Listing products: search=%s, section=%s, filters=[size=%s, color=%s, style=%s, gender=%s, condition=%s]",
        search, section, size, color, style, gender, condition
    )
    products = crud.list_products(
        db,
        search=search,
        category_id=category_id,
        section=section,
        size=size,
        color=color,
        style=style,
        gender=gender,
        condition=condition,
        skip=skip,
        limit=limit
    )
    
    # Добавляем seller_username/contact для каждого товара
    for product in products:
        if product.seller:
            if not product.seller_username:
                product.seller_username = product.seller.username
            if not product.seller_contact:
                product.seller_contact = product.seller.contact
    
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """Получить товар по ID"""
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Добавляем username/contact продавца в response
    if product.seller:
        if not product.seller_username:
            product.seller_username = product.seller.username
        if not product.seller_contact:
            product.seller_contact = product.seller.contact
    return product
