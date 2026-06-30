"""Project configuration loaded from environment variables."""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME", "")
GCP_RAW_PREFIX = os.getenv("GCP_RAW_PREFIX", "raw/mvtec")
GCP_PROCESSED_PREFIX = os.getenv("GCP_PROCESSED_PREFIX", "processed")
GCP_MODEL_PREFIX = os.getenv("GCP_MODEL_PREFIX", "models")
LOCAL_DATA_DIR = Path(os.getenv("LOCAL_DATA_DIR", "data/raw/mvtec"))


def require_env(name: str, value: str) -> str:
    """Raise a clear error when a required environment variable is missing."""
    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            "Create a .env file from .env.example and update it."
        )
    return value
