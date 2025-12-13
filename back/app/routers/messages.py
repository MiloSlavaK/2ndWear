from fastapi import APIRouter, Depends
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


@router.post("/", response_model=schemas.Message)
def send_message(data: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, data)


@router.get("/product/{product_id}", response_model=list[schemas.Message])
def get_messages_by_product(product_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Message)
        .filter(models.Message.product_id == product_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )