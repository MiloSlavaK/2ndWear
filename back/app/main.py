# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import users, products, orders, messages, categories, media
from .logger import setup_logging
import logging
from fastapi import Request
import time
import os


setup_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="2ndWear API", version="1.0.0")

# CORS: разрешить запросы с фронтенда
# В продакшене используй конкретные домены вместо "*"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL", "http://localhost:3000")

# Получаем внешний URL из переменной окружения (для деплоя)
EXTERNAL_FRONTEND_URL = os.getenv("EXTERNAL_FRONTEND_URL", "")

# Формируем список разрешенных origins
allowed_origins = [FRONTEND_URL, TELEGRAM_BOT_URL, "http://localhost:5173", "http://localhost:3000"]
if EXTERNAL_FRONTEND_URL:
    allowed_origins.append(EXTERNAL_FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        "%s %s - %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response


# Регистрация роутеров
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])


@app.get("/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok", "service": "2ndWear Backend"}


logger.info("2ndWear backend started")
