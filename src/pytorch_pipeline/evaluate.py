"""
PyTorch evaluation pipeline with MLflow tracking.
"""

import csv
from pathlib import Path

import mlflow
import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix

from app.config import DEFAULT_MODEL_VERSION
from src.common.config import PROCESSED_DATA_DIR, REPORTS_DIR
from src.pytorch_pipeline.data_loader import load_pytorch_datasets
from src.pytorch_pipeline.model import build_resnet18_model

MODEL_DIR = Path("models")


def evaluate_pytorch_model(
    category: str = "bottle",
    model_version: str = DEFAULT_MODEL_VERSION,
):
    dataset_path = PROCESSED_DATA_DIR / category
    model_path = MODEL_DIR / "pytorch" / category / model_version / "model.pt"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    _, validation_loader, class_names, device = load_pytorch_datasets(
        dataset_path=dataset_path,
        batch_size=32,
    )

    model = build_resnet18_model(num_classes=len(class_names))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():
        for images, labels in validation_loader:
            images = images.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            y_true.extend(labels.numpy())
            y_pred.extend(predicted.cpu().numpy())

    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(y_true, y_pred)

    report_path = REPORTS_DIR / "pytorch_classification_report.csv"
    matrix_path = REPORTS_DIR / "pytorch_confusion_matrix.csv"

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

    np.savetxt(matrix_path, matrix, delimiter=",", fmt="%d")

    mlflow.set_experiment("Industrial Defect Detection")

    with mlflow.start_run(run_name=f"pytorch_evaluation_{category}_{model_version}"):
        mlflow.log_param("framework", "PyTorch")
        mlflow.log_param("model", "ResNet18")
        mlflow.log_param("category", category)
        mlflow.log_param("model_version", model_version)

        mlflow.log_metric("accuracy", report["accuracy"])
        mlflow.log_metric("macro_f1", report["macro avg"]["f1-score"])
        mlflow.log_metric("weighted_f1", report["weighted avg"]["f1-score"])

        mlflow.log_artifact(str(report_path))
        mlflow.log_artifact(str(matrix_path))

    print(f"PyTorch classification report saved to: {report_path}")
    print(f"PyTorch confusion matrix saved to: {matrix_path}")
