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



@router.post("/", response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == data.username).first()
    if existing:
        logger.warning("Attempt to create duplicate user: %s", data.username)
        raise HTTPException(status_code=400, detail="Username already exists")

    return crud.create_user(db, data)


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/telegram/{telegram_id}", response_model=schemas.User)
def get_or_create_telegram_user(telegram_id: str, data: schemas.UserCreate | None = None, db: Session = Depends(get_db)):
    """Endpoint for Telegram bot to sync username/contact."""
    username = data.username if data else None
    contact = data.contact if data else None
    return crud.get_or_create_user(db, telegram_id, username=username, contact=contact)