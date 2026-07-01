"""
Preprocess MVTec AD into binary classification folders.
"""

import random
import shutil
from pathlib import Path

from .config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
    RANDOM_SEED,
)

SOURCE_CATEGORY = "bottle"


def copy_images(images, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)

    for image_path in images:
        target_path = destination / image_path.name
        shutil.copy2(image_path, target_path)


def create_binary_classification_dataset(category: str = SOURCE_CATEGORY):
    random.seed(RANDOM_SEED)

    raw_category_path = RAW_DATA_DIR / "mvtec_ad" / category

    good_images = list((raw_category_path / "train" / "good").glob("*.png"))
    defective_images = [
        path
        for path in (raw_category_path / "test").glob("*/*.png")
        if "good" not in str(path)
    ]

    random.shuffle(good_images)
    random.shuffle(defective_images)

    def split_images(images):
        train_end = int(len(images) * TRAIN_SPLIT)
        val_end = int(len(images) * (TRAIN_SPLIT + VALIDATION_SPLIT))

        return (
            images[:train_end],
            images[train_end:val_end],
            images[val_end:],
        )

    good_train, good_val, good_test = split_images(good_images)
    defect_train, defect_val, defect_test = split_images(defective_images)

    if PROCESSED_DATA_DIR.exists():
        shutil.rmtree(PROCESSED_DATA_DIR)

    copy_images(good_train, PROCESSED_DATA_DIR / "train" / "good")
    copy_images(good_val, PROCESSED_DATA_DIR / "validation" / "good")
    copy_images(good_test, PROCESSED_DATA_DIR / "test" / "good")

    copy_images(defect_train, PROCESSED_DATA_DIR / "train" / "defective")
    copy_images(defect_val, PROCESSED_DATA_DIR / "validation" / "defective")
    copy_images(defect_test, PROCESSED_DATA_DIR / "test" / "defective")

    print("Processed dataset created.")
    print(f"Category: {category}")
    print(f"Good images: {len(good_images)}")
    print(f"Defective images: {len(defective_images)}")


if __name__ == "__main__":
    create_binary_classification_dataset()