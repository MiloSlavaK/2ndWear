# app/routers/categories.py
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


@router.post("/", response_model=schemas.Category)
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    logger.info("Creating category: name=%s", data.name)
    return crud.create_category(db, data.name)


@router.get("/", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    """Получить все категории"""
    return crud.list_categories(db)


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
