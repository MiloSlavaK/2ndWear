from fastapi import FastAPI
from .db import Base, engine
from .routers import users, products, orders, messages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="2ndWear API")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
