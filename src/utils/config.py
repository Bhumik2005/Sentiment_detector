"""Centralized configuration management with Pydantic settings."""
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "sentiment-mlops-pipeline"
    ENV: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = False
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    API_MAX_REQUEST_SIZE: int = 10 * 1024 * 1024
    MODEL_NAME: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MODEL_VERSION: str = "latest"
    MODEL_MAX_LENGTH: int = 512
    MODEL_BATCH_SIZE: int = 32
    MODEL_CONFIDENCE_THRESHOLD: float = 0.7
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_FEATURE_TTL: int = 3600
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_INPUT: str = "social-media-raw"
    KAFKA_TOPIC_OUTPUT: str = "sentiment-predictions"
    KAFKA_CONSUMER_GROUP: str = "sentiment-processor-v1"
    KAFKA_MAX_POLL_RECORDS: int = 500
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "sentiment-analysis"
    MLFLOW_REGISTERED_MODEL_NAME: str = "sentiment-classifier"
    PROMETHEUS_PORT: int = 9090
    PROMETHEUS_MULTIPROC_DIR: str = "/tmp/prometheus"
    DRIFT_DETECTION_WINDOW: int = 1000
    DRIFT_THRESHOLD: float = 0.05
    ALERT_WEBHOOK_URL: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = "http://localhost:9000"
    S3_BUCKET_NAME: str = "mlflow-artifacts"
    S3_ACCESS_KEY: str = "minio"
    S3_SECRET_KEY: str = "minio123"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    MODEL_A_WEIGHT: float = 0.5
    MODEL_B_WEIGHT: float = 0.5
    MODEL_B_NAME: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()