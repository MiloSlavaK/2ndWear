# app/services/storage.py
import os
import io
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
        """Upload bytes to storage and return image_key (for secure backend proxy)."""
        object_name = f"{uuid.uuid4().hex}.jpg"
        data_stream = io.BytesIO(data)
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=data_stream,
            length=len(data),
            content_type=content_type,
        )

        return {
            "key": object_name,
            "url": f"/media/download/{object_name}"  # Backend proxy path
        }

    def get_object(self, object_name: str) -> tuple:
        """Retrieve file from storage (for backend proxy).
        
        Returns tuple of (bytes, content_length) to properly stream with Content-Length header.
        """
        response = self.client.get_object(self.bucket, object_name)
        file_data = response.read()
        # Ensure response is properly closed
        response.close()
        response.release_conn()
        return file_data, len(file_data)
