from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import SessionLocal
from .. import crud, schemas, models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Order)
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return crud.create_order(db, data)


@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/{order_id}/summary")
def order_summary(order_id: int, db: Session = Depends(get_db)):
    """
    Демонстрационный эндпоинт для питча:
    показывает комиссию и распределение денег.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    fee = round(product.price * 0.1, 2)

    return {
        "order_id": order.id,
        "product_price": product.price,
        "platform_fee": fee,
        "seller_receives": product.price - fee,
        "status": order.status
    }