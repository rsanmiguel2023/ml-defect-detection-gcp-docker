"""
TensorFlow Dataset Loader

Loads preprocessed train and validation image folders.
"""

import tensorflow as tf

from .config import BATCH_SIZE, IMAGE_SIZE


def load_datasets(dataset_path: str):
    """
    Load training and validation datasets from a processed category directory.

    Expected structure:
    dataset_path/
        train/
            good/
            defective/
        validation/
            good/
            defective/
    """

    train_ds = tf.keras.utils.image_dataset_from_directory(
        f"{dataset_path}/train",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    validation_ds = tf.keras.utils.image_dataset_from_directory(
        f"{dataset_path}/validation",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    class_names = train_ds.class_names

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, validation_ds, class_names
