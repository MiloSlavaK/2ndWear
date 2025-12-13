# app/routers/products.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Product)
def create_product(data: schemas.ProductCreate, seller_id: int, db: Session = Depends(get_db)):
    return crud.create_product(db, data, seller_id)


@router.get("/", response_model=list[schemas.Product])
def list_products(search: str | None = None, category: str | None = None, db: Session = Depends(get_db)):
    return crud.list_products(db, search, category)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    return product
