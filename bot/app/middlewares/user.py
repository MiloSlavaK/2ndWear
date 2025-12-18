import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

from app.api.backend import BackendAPI

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        self.api = BackendAPI()

    async def __call__(self, handler, event: Update, data: dict):
        logger.info("UserMiddleware triggered")

        telegram_user = None

        if event.message:
            telegram_user = event.message.from_user
        elif event.callback_query:
            telegram_user = event.callback_query.from_user

        if telegram_user is None:
            return await handler(event, data)

        telegram_id = telegram_user.id

        try:
            user = await self.api.get_or_create_user(telegram_id)
        except Exception:
            logger.exception(
                "Failed to sync user with backend, continue without user: telegram_id=%s",
                telegram_id,
            )
            data["user"] = None
            data["user_id"] = None
            return await handler(event, data)

        data["user"] = user
        data["user_id"] = user["id"]

        logger.info(
            "User synced: telegram_id=%s backend_user_id=%s",
            telegram_id,
            user["id"],
        )

        return await handler(event, data)
