# app/services/storage.py
import os
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
import uuid


class MinioStorage:
    """S3-compatible storage wrapper for images."""

    def __init__(self):
        endpoint = os.getenv("MINIO_ENDPOINT", "http://localhost:9000").replace("https://", "").replace("http://", "")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        bucket = os.getenv("MINIO_BUCKET", "products")
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"

        self.bucket = bucket
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

        # Ensure bucket exists
        found = self.client.bucket_exists(self.bucket)
        if not found:
            self.client.make_bucket(self.bucket)

    def upload_bytes(self, data: bytes, content_type: str = "image/jpeg") -> dict:
        """Upload bytes to storage and return public URL and key."""
        object_name = f"{uuid.uuid4().hex}.jpg"
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=data,
            length=len(data),
            content_type=content_type,
        )

        return {
            "key": object_name,
            "url": self.get_presigned_url(object_name)
        }

    def get_presigned_url(self, object_name: str, expires: int = 60 * 60 * 24 * 7) -> str:
        """Generate presigned URL for object (default 7 days)."""
        return self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=object_name,
            expires=timedelta(seconds=expires),
        )
