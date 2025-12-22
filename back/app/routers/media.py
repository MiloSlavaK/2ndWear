# app/routers/media.py
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from ..services.storage import MinioStorage
import io

router = APIRouter()
logger = logging.getLogger(__name__)
storage = MinioStorage()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload image to MinIO and return download path."""
    try:
        content = await file.read()
        result = storage.upload_bytes(content, content_type=file.content_type or "image/jpeg")
        logger.info("Image uploaded to storage: key=%s", result["key"])
        return {"image_url": result["url"], "image_key": result["key"]}
    except Exception as e:
        logger.exception("Failed to upload image: %s", e)
        raise HTTPException(status_code=500, detail="Failed to upload image")


@router.get("/download/{image_key}")
async def download_image(image_key: str):
    """Download image from MinIO (backend proxy for security)."""
    try:
        # Validate image_key to prevent directory traversal
        if "/" in image_key or ".." in image_key:
            raise HTTPException(status_code=400, detail="Invalid image key")
        
        logger.info("Downloading image: key=%s", image_key)
        
        # Retrieve from MinIO
        image_bytes = storage.get_object(image_key)
        
        # Stream back to client
        return StreamingResponse(
            io.BytesIO(image_bytes),
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=86400"}  # Cache for 1 day
        )
    except Exception as e:
        logger.exception("Failed to download image: %s", e)
        raise HTTPException(status_code=404, detail="Image not found")
