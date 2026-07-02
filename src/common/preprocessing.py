"""
Preprocess MVTec AD into category-specific binary classification folders.
"""

import random
import shutil
from pathlib import Path

from .config import (
    PROCESSED_DATA_DIR,
    RANDOM_SEED,
    RAW_DATA_DIR,
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
)

CATEGORIES = [
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


def copy_images(images, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)

    for image_path in images:
        target_path = destination / image_path.name
        shutil.copy2(image_path, target_path)


def split_images(images):
    train_end = int(len(images) * TRAIN_SPLIT)
    val_end = int(len(images) * (TRAIN_SPLIT + VALIDATION_SPLIT))

    return (
        images[:train_end],
        images[train_end:val_end],
        images[val_end:],
    )


def process_category(category: str):
    raw_category_path = RAW_DATA_DIR / "mvtec_ad" / category
    processed_category_path = PROCESSED_DATA_DIR / category

    good_images = list((raw_category_path / "train" / "good").glob("*.png"))

    defective_images = [
        path
        for path in (raw_category_path / "test").glob("*/*.png")
        if "good" not in str(path)
    ]

    random.shuffle(good_images)
    random.shuffle(defective_images)

    good_train, good_val, good_test = split_images(good_images)
    defect_train, defect_val, defect_test = split_images(defective_images)

    if processed_category_path.exists():
        shutil.rmtree(processed_category_path)

    copy_images(good_train, processed_category_path / "train" / "good")
    copy_images(good_val, processed_category_path / "validation" / "good")
    copy_images(good_test, processed_category_path / "test" / "good")

    copy_images(defect_train, processed_category_path / "train" / "defective")
    copy_images(defect_val, processed_category_path / "validation" / "defective")
    copy_images(defect_test, processed_category_path / "test" / "defective")

    print(f"{category}: good={len(good_images)}, defective={len(defective_images)}")


def create_all_binary_datasets():
    random.seed(RANDOM_SEED)

    for category in CATEGORIES:
        process_category(category)

    print("All category datasets created.")


if __name__ == "__main__":
    create_all_binary_datasets()
