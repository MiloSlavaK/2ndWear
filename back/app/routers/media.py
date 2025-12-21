# app/routers/media.py
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.storage import MinioStorage

router = APIRouter()
logger = logging.getLogger(__name__)
storage = MinioStorage()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = storage.upload_bytes(content, content_type=file.content_type or "image/jpeg")
        logger.info("Image uploaded to storage: key=%s", result["key"])
        return {"image_url": result["url"], "image_key": result["key"]}
    except Exception as e:
        logger.exception("Failed to upload image: %s", e)
        raise HTTPException(status_code=500, detail="Failed to upload image")
