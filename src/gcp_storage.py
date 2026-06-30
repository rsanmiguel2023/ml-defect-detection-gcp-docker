"""Utilities for working with Google Cloud Storage."""

from pathlib import Path
from google.cloud import storage

from src.config import GCP_BUCKET_NAME, GCP_RAW_PREFIX, LOCAL_DATA_DIR, require_env


def get_storage_client() -> storage.Client:
    """Create a Google Cloud Storage client using local credentials."""
    return storage.Client()


def get_bucket() -> storage.Bucket:
    """Return the configured GCS bucket."""
    bucket_name = require_env("GCP_BUCKET_NAME", GCP_BUCKET_NAME)
    client = get_storage_client()
    return client.bucket(bucket_name)


def list_blobs(prefix: str = GCP_RAW_PREFIX, limit: int = 20) -> list[str]:
    """List a small sample of objects under a GCS prefix."""
    bucket = get_bucket()
    blobs = bucket.list_blobs(prefix=prefix, max_results=limit)
    return [blob.name for blob in blobs]


def download_prefix(prefix: str = GCP_RAW_PREFIX, destination: Path = LOCAL_DATA_DIR) -> int:
    """Download objects from a GCS prefix into a local folder."""
    bucket = get_bucket()
    count = 0

    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.endswith("/"):
            continue

        relative_path = blob.name.removeprefix(prefix).lstrip("/")
        local_path = destination / relative_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(local_path)
        count += 1

    return count
