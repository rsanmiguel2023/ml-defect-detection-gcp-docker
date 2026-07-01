"""
Dataset ingestion and validation utilities for the MVTec AD dataset.
"""

from pathlib import Path

from .config import RAW_DATA_DIR, DATASET_PREFIX
from .gcs import GCSStorage


EXPECTED_CATEGORIES = [
    "bottle",
    "cable",
    "capsule",
    "carpet",
    "grid",
    "hazelnut",
    "leather",
    "metal_nut",
    "pill",
    "screw",
    "tile",
    "toothbrush",
    "transistor",
    "wood",
    "zipper",
]


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


def validate_raw_dataset() -> bool:
    """
    Validate expected MVTec AD category folders exist locally.
    """

    dataset_path = RAW_DATA_DIR / "mvtec_ad"

    missing_categories = []

    for category in EXPECTED_CATEGORIES:
        category_path = dataset_path / category

        if not category_path.exists():
            missing_categories.append(category)

    if missing_categories:
        print("Missing categories:")
        for category in missing_categories:
            print(f"- {category}")

        return False

    print("Dataset validation passed.")
    return True


if __name__ == "__main__":
    download_raw_dataset()
    validate_raw_dataset()