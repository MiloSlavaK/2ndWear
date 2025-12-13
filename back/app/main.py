# app/main.py
from fastapi import FastAPI
from .db import Base, engine
from .routers import users, products, orders, messages
from .logger import setup_logging
import logging
from fastapi import Request
import time


setup_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="2ndWear API")


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


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

logger.info("2ndWear backend started")
