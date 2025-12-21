import httpx
from app.config.settings import settings
import logging
logger = logging.getLogger(__name__)


class BackendAPI:
    def __init__(self):
        self.base_url = settings.backend_api_url

    async def get_or_create_user(self, telegram_id: int, username: str | None = None, contact: str | None = None):
        payload = {
            "username": username,
            "contact": contact,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/users/telegram/{telegram_id}", json=payload
            )
            response.raise_for_status()
            return response.json()

    async def list_products(self, section: str = "market", limit: int = 10) -> list:
        """
        Получить список товаров из backend
        """
        url = f"{self.base_url}/products/"
        params = {
            "section": section,
            "limit": limit,
        }

        logger.info("Fetching products: section=%s limit=%s", section, limit)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                products = response.json()
                logger.info("Retrieved %s products from backend", len(products))
                return products
        except httpx.HTTPError as e:
            logger.error("Error fetching products: %s", e)
            return []

    async def create_product(self, seller_id: str, data: dict) -> dict:
        url = f"{self.base_url}/products/"

        payload = {
            "title": data["title"],
            "price": data["price"],
            "description": data["description"],
            "category": data.get("category"),
            "size": data.get("size", ""),
            "color": data.get("color", ""),
            "style": data.get("style", ""),
            "gender": data.get("gender", ""),
            "condition": data.get("condition", ""),
            "section": data.get("section", "market"),
            "image_url": data.get("image_url"),
            "image_key": data.get("image_key"),
            "seller_username": data.get("seller_username"),
            "seller_contact": data.get("seller_contact"),
        }   

        params = {
            "seller_id": seller_id
        }

        logger.info(
            "Sending product to backend: seller_id=%s title=%s",
            seller_id,
            payload.get("title"),
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

    async def upload_image(self, file_bytes: bytes, filename: str, content_type: str | None = None) -> dict:
        url = f"{self.base_url}/media/upload"
        files = {"file": (filename, file_bytes, content_type or "image/jpeg")}
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, files=files)
        response.raise_for_status()
        return response.json()