"""
Dataset ingestion, validation, and summary utilities for MVTec AD.
"""

import json
from pathlib import Path

from .config import RAW_DATA_DIR, REPORTS_DIR, DATASET_PREFIX
from .gcs import GCSStorage


EXPECTED_CATEGORIES = [
    "bottle", "cable", "capsule", "carpet", "grid",
    "hazelnut", "leather", "metal_nut", "pill", "screw",
    "tile", "toothbrush", "transistor", "wood", "zipper",
]


def download_raw_dataset() -> int:
    storage = GCSStorage()

    downloaded_count = storage.download_folder(
        prefix=DATASET_PREFIX,
        local_directory=RAW_DATA_DIR / "mvtec_ad",
    )

    print(f"Downloaded {downloaded_count} new files.")
    return downloaded_count


def validate_raw_dataset() -> bool:
    dataset_path = RAW_DATA_DIR / "mvtec_ad"
    missing_categories = []

    for category in EXPECTED_CATEGORIES:
        if not (dataset_path / category).exists():
            missing_categories.append(category)

    if missing_categories:
        print("Missing categories:")
        for category in missing_categories:
            print(f"- {category}")
        return False

    print("Dataset validation passed.")
    return True


def generate_dataset_summary() -> dict:
    dataset_path = RAW_DATA_DIR / "mvtec_ad"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    summary = {}

    for category in EXPECTED_CATEGORIES:
        category_path = dataset_path / category

        train_good = list((category_path / "train" / "good").glob("*.png"))
        test_images = list((category_path / "test").glob("*/*.png"))
        ground_truth = list((category_path / "ground_truth").glob("*/*.png"))

        summary[category] = {
            "train_good_images": len(train_good),
            "test_images": len(test_images),
            "ground_truth_masks": len(ground_truth),
        }

    output_path = REPORTS_DIR / "dataset_summary.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print(f"Dataset summary saved to: {output_path}")
    return summary


if __name__ == "__main__":
    download_raw_dataset()
    validate_raw_dataset()
    generate_dataset_summary()