import asyncio
from aiogram import Bot, Dispatcher
from app.config.settings import settings
from app.handlers.start import router as start_router
from app.middlewares.user import UserMiddleware
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)

storage = RedisStorage(redis_client)
dp = Dispatcher(storage=storage)

async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.message.middleware(UserMiddleware())

    dp.include_router(start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
