from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import logging
from app.api.backend import BackendAPI

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        self.api = BackendAPI()

    async def __call__(self, handler, event: TelegramObject, data: dict):
        if hasattr(event, "from_user") and event.from_user:
            tg_id = event.from_user.id

            try:
                user = await self.api.get_or_create_user(tg_id)
                data["user"] = user
            except Exception as e:
                logger.warning(
                    "Failed to sync user with backend: telegram_id=%s, error=%s",
                    tg_id,
                    repr(e),
                )
        return await handler(event, data)

