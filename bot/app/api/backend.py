import httpx
from app.config.settings import settings


class BackendAPI:
    def __init__(self):
        self.base_url = settings.backend_api_url

    async def get_or_create_user(self, telegram_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/users/telegram/{telegram_id}"
            )
            response.raise_for_status()
            return response.json()