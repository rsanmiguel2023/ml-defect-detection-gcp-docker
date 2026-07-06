"""
Train TensorFlow EfficientNetB0 model for defect classification.
"""

import mlflow
import tensorflow as tf

from app.config import DEFAULT_MODEL_VERSION

from .config import DATA_DIR, EPOCHS, MODEL_DIR, REPORT_DIR
from .data_loader import load_datasets
from .model import build_efficientnet_model


def train_tensorflow_model(
    category: str = "bottle",
    model_version: str = DEFAULT_MODEL_VERSION,
):
    """
    Train and save the TensorFlow EfficientNetB0 model.
    """

    dataset_path = DATA_DIR / "processed" / category

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    versioned_model_dir = MODEL_DIR / "tensorflow" / category / model_version
    versioned_model_dir.mkdir(parents=True, exist_ok=True)

    model_path = versioned_model_dir / "model.keras"

    train_ds, validation_ds, class_names = load_datasets(str(dataset_path))

    model = build_efficientnet_model(num_classes=len(class_names))

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(model_path),
            monitor="val_accuracy",
            save_best_only=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-6,
        ),
    ]

    mlflow.set_experiment("Industrial Defect Detection")

    with mlflow.start_run(
        run_name=f"tensorflow_efficientnet_{category}_{model_version}"
    ):
        mlflow.log_param("framework", "TensorFlow")
        mlflow.log_param("model", "EfficientNetB0")
        mlflow.log_param("category", category)
        mlflow.log_param("model_version", model_version)
        mlflow.log_param("epochs", EPOCHS)

        history = model.fit(
            train_ds,
            validation_data=validation_ds,
            epochs=EPOCHS,
            callbacks=callbacks,
        )

        final_epoch = len(history.history["accuracy"]) - 1

        mlflow.log_metric(
            "train_accuracy",
            history.history["accuracy"][final_epoch],
        )
        mlflow.log_metric(
            "train_loss",
            history.history["loss"][final_epoch],
        )
        mlflow.log_metric(
            "val_accuracy",
            history.history["val_accuracy"][final_epoch],
        )
        mlflow.log_metric(
            "val_loss",
            history.history["val_loss"][final_epoch],
        )

        mlflow.log_artifact(str(model_path))

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

    print(f"TensorFlow model saved to: {model_path}")
    print(f"Training history saved to: {history_path}")


if __name__ == "__main__":
    train_tensorflow_model()
