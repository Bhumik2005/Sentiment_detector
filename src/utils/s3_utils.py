"""S3/MinIO utilities for model artifact management."""
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional
import tempfile
import os

from src.utils.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class S3Client:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(max_pool_connections=50, retries={"max_attempts": 3, "mode": "adaptive"}),
        )
        self.bucket = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.client.create_bucket(Bucket=self.bucket)
                logger.info(f"Created S3 bucket: {self.bucket}")
    
    def upload_model(self, local_path: str, model_version: str) -> str:
        s3_key = f"models/sentiment-classifier/{model_version}/model.pt"
        try:
            self.client.upload_file(local_path, self.bucket, s3_key)
            logger.info(f"Uploaded model to s3://{self.bucket}/{s3_key}")
            return s3_key
        except ClientError as e:
            logger.error(f"Failed to upload model: {e}")
            raise
    
    def download_model(self, model_version: str, destination: Optional[str] = None) -> str:
        s3_key = f"models/sentiment-classifier/{model_version}/model.pt"
        if destination is None:
            destination = tempfile.mkdtemp()
        local_path = os.path.join(destination, "model.pt")
        try:
            self.client.download_file(self.bucket, s3_key, local_path)
            logger.info(f"Downloaded model to {local_path}")
            return local_path
        except ClientError as e:
            logger.error(f"Failed to download model: {e}")
            raise


_s3_client: Optional[S3Client] = None

def get_s3_client() -> S3Client:
    global _s3_client
    if _s3_client is None:
        _s3_client = S3Client()
    return _s3_client