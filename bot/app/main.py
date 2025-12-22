from app.config.logging import setup_logging
setup_logging()

import asyncio
from aiogram import Bot, Dispatcher
from app.config.settings import settings

from app.handlers.start import router as start_router
from app.handlers.add_product import router as add_product_router
from app.handlers.buy import router as buy_router
from app.handlers.common import router as common_router

from app.middlewares.user import UserMiddleware

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)

storage = RedisStorage(redis_client)

async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=storage)
    dp.update.middleware(UserMiddleware())

    dp.include_router(start_router)
    dp.include_router(common_router)
    dp.include_router(add_product_router)
    dp.include_router(buy_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
