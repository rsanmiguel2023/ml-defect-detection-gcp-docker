"""
Dataset ingestion utilities for the MVTec AD dataset.
"""

from pathlib import Path

from .config import RAW_DATA_DIR, DATASET_PREFIX
from .gcs import GCSStorage


def download_raw_dataset() -> int:
    """
    Download the raw MVTec AD dataset from Google Cloud Storage.
    """

    storage = GCSStorage()

    downloaded_count = storage.download_folder(
        prefix=DATASET_PREFIX,
        local_directory=RAW_DATA_DIR / "mvtec_ad"
    )

    print(f"Downloaded {downloaded_count} new files.")

    return downloaded_count


if __name__ == "__main__":
    download_raw_dataset()