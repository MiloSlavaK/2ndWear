import os
import httpx 
import logging

logger = logging.getLogger(__name__)

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000") 

async def get_or_create_user_in_backend(telegram_id: int):
    url = f"{API_URL}/users/telegram/{telegram_id}"
    logger.info(f"Connecting to API URL: {url}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url) 
            response.raise_for_status() # Вызывает исключение для 4xx/5xx ошибок
            
            user_data = response.json()
            return user_data.get('id') 

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Error connecting to backend: {e}")
        return None
        

async def create_product_in_backend(product_data: dict, seller_db_id: int):
    """Отправляет запрос на создание продукта"""
    url = f"{API_URL}/products/"
    params = {"seller_id": seller_db_id} 
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=product_data, params=params)
        response.raise_for_status()
        return response.json()
