"""
Google Cloud Storage client for dataset and model management.
"""

from pathlib import Path

from google.cloud import storage

from .config import GCP_PROJECT, GCS_BUCKET


class GCSStorage:

    def __init__(self):

        self.client = storage.Client(project=GCP_PROJECT)

        self.bucket = self.client.bucket(GCS_BUCKET)

    def list_objects(self, prefix: str):

        blobs = self.client.list_blobs(self.bucket, prefix=prefix)

        return [blob.name for blob in blobs]

    def download_folder(self, prefix: str, local_directory: Path):

        local_directory.mkdir(parents=True, exist_ok=True)

        downloaded = 0

        blobs = self.client.list_blobs(self.bucket, prefix=prefix)

        for blob in blobs:

            if blob.name.endswith("/"):
                continue

            relative = blob.name.replace(prefix, "").lstrip("/")

            destination = local_directory / relative

            destination.parent.mkdir(parents=True, exist_ok=True)

            if destination.exists():
                continue

            blob.download_to_filename(destination)

            downloaded += 1

        return downloaded

    def upload_file(self, local_file: Path, destination: str):

        blob = self.bucket.blob(destination)

        blob.upload_from_filename(local_file)
