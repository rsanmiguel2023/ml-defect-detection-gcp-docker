"""
TensorFlow Dataset Loader

Loads image datasets for training and validation.
"""

import tensorflow as tf

from .config import (
    IMAGE_SIZE,
    BATCH_SIZE,
    TRAIN_SPLIT,
    RANDOM_SEED
)


def load_datasets(dataset_path: str):
    """
    Load training and validation datasets from a directory.
    """

    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=1 - TRAIN_SPLIT,
        subset="training",
        seed=RANDOM_SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    validation_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=1 - TRAIN_SPLIT,
        subset="validation",
        seed=RANDOM_SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = (
        train_ds
        .cache()
        .shuffle(1000)
        .prefetch(buffer_size=AUTOTUNE)
    )

    validation_ds = (
        validation_ds
        .cache()
        .prefetch(buffer_size=AUTOTUNE)
    )

    return train_ds, validation_ds, class_names