import httpx
from app.config.settings import settings
import logging
logger = logging.getLogger(__name__)


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

    async def create_product(self, seller_id: int, data: dict) -> dict:
        url = f"{self.base_url}/products/"

        payload = {
            "title": data["title"],
            "price": data["price"],
            "description": data["description"],
            "category": data["category"],
            "image_url": data["image_url"],
        }   

        params = {
            "seller_id": seller_id
        }

        logger.info(
            "Sending product to backend: seller_id=%s payload=%s",
            seller_id,
            payload,
        )

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, params=params)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(
                "Backend error while creating product: status=%s body=%s",
                response.status_code,
                response.text,
            )
            raise

        return response.json()