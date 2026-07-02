"""
Train TensorFlow EfficientNetB0 model for defect classification.
"""

from pathlib import Path

import tensorflow as tf

from .config import (
    DATA_DIR,
    MODEL_DIR,
    REPORT_DIR,
    EPOCHS,
    MODEL_FILENAME
)
from .data_loader import load_datasets
from .model import build_efficientnet_model


def train_tensorflow_model(category: str = "bottle"):
    """
    Train and save the TensorFlow EfficientNetB0 model.
    """

    dataset_path = DATA_DIR / "processed" / category

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    train_ds, validation_ds, class_names = load_datasets(str(dataset_path))

    model = build_efficientnet_model(num_classes=len(class_names))

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(MODEL_DIR / MODEL_FILENAME),
            monitor="val_accuracy",
            save_best_only=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-6
        )
    ]

    history = model.fit(
        train_ds,
        validation_data=validation_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    history_path = REPORT_DIR / "tensorflow_training_history.csv"

    with open(history_path, "w", encoding="utf-8") as file:
        file.write("epoch,accuracy,loss,val_accuracy,val_loss\n")

        for epoch in range(len(history.history["accuracy"])):
            file.write(
                f"{epoch + 1},"
                f"{history.history['accuracy'][epoch]},"
                f"{history.history['loss'][epoch]},"
                f"{history.history['val_accuracy'][epoch]},"
                f"{history.history['val_loss'][epoch]}\n"
            )

    print(f"TensorFlow model saved to: {MODEL_DIR / MODEL_FILENAME}")
    print(f"Training history saved to: {history_path}")


if __name__ == "__main__":
    train_tensorflow_model()