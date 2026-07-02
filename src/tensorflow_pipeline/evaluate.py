"""
Evaluate TensorFlow EfficientNetB0 model.
"""

import csv

import mlflow
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from .config import DATA_DIR, MODEL_DIR, MODEL_FILENAME, REPORT_DIR
from .data_loader import load_datasets


def evaluate_tensorflow_model(category: str = "bottle"):
    """
    Evaluate the trained TensorFlow model and save metrics.
    """

    dataset_path = DATA_DIR / "processed" / category
    model_path = MODEL_DIR / MODEL_FILENAME

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    _, validation_ds, class_names = load_datasets(str(dataset_path))

    model = tf.keras.models.load_model(model_path)

    y_true = []
    y_pred = []

    for images, labels in validation_ds:
        predictions = model.predict(images)
        predicted_classes = np.argmax(predictions, axis=1)

        y_true.extend(labels.numpy())
        y_pred.extend(predicted_classes)

    report = classification_report(
        y_true, y_pred, target_names=class_names, output_dict=True
    )

    mlflow.set_experiment("Industrial Defect Detection")

    with mlflow.start_run(run_name=f"tensorflow_evaluation_{category}"):
        mlflow.log_param("framework", "TensorFlow")
        mlflow.log_param("model", "EfficientNetB0")
        mlflow.log_param("category", category)

        accuracy = report["accuracy"]
        macro_f1 = report["macro avg"]["f1-score"]
        weighted_f1 = report["weighted avg"]["f1-score"]

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("macro_f1", macro_f1)
        mlflow.log_metric("weighted_f1", weighted_f1)

        report_path = REPORT_DIR / "tensorflow_classification_report.csv"

        with open(report_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["class", "precision", "recall", "f1_score", "support"])

            for class_name, metrics in report.items():
                if isinstance(metrics, dict):
                    writer.writerow(
                        [
                            class_name,
                            metrics.get("precision"),
                            metrics.get("recall"),
                            metrics.get("f1-score"),
                            metrics.get("support"),
                        ]
                    )

        matrix = confusion_matrix(y_true, y_pred)
        matrix_path = REPORT_DIR / "tensorflow_confusion_matrix.csv"

        np.savetxt(matrix_path, matrix, delimiter=",", fmt="%d")

        mlflow.log_artifact(str(report_path))
        mlflow.log_artifact(str(matrix_path))

    print(f"Classification report saved to: {report_path}")
    print(f"Confusion matrix saved to: {matrix_path}")


if __name__ == "__main__":
    evaluate_tensorflow_model()
