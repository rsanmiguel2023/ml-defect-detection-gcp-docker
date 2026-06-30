from pathlib import Path
from google.cloud import storage
from src.config import settings


def _client() -> storage.Client:
    if settings.gcp_project_id:
        return storage.Client(project=settings.gcp_project_id)
    return storage.Client()


def download_prefix(prefix: str | None = None, destination_dir: str | None = None) -> None:
    """Download all objects under a GCS prefix into a local directory."""
    bucket_name = settings.gcp_bucket_name
    if not bucket_name:
        raise ValueError("GCP_BUCKET_NAME is not set. Add it to your .env file.")

    prefix = prefix or settings.gcp_raw_prefix
    destination = Path(destination_dir or settings.local_data_dir)
    destination.mkdir(parents=True, exist_ok=True)

    client = _client()
    bucket = client.bucket(bucket_name)

    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.endswith("/"):
            continue
        relative_path = Path(blob.name).relative_to(prefix)
        local_path = destination / relative_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(local_path)

    print(f"Downloaded gs://{bucket_name}/{prefix} to {destination}")


def upload_file(local_file: str, destination_blob: str) -> None:
    """Upload one local file to the configured GCS bucket."""
    bucket_name = settings.gcp_bucket_name
    if not bucket_name:
        raise ValueError("GCP_BUCKET_NAME is not set. Add it to your .env file.")

    client = _client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(local_file)
    print(f"Uploaded {local_file} to gs://{bucket_name}/{destination_blob}")
