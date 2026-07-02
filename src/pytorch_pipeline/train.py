"""
PyTorch training pipeline with MLflow tracking.
"""

from pathlib import Path

import mlflow
import torch
import torch.nn as nn
import torch.optim as optim

from src.common.config import PROCESSED_DATA_DIR
from src.pytorch_pipeline.data_loader import load_pytorch_datasets
from src.pytorch_pipeline.model import build_resnet18_model

MODEL_DIR = Path("models")
MODEL_FILENAME = "resnet18_pytorch.pt"
EPOCHS = 10
LEARNING_RATE = 0.0001
BATCH_SIZE = 32


def train_pytorch_model(category: str = "bottle"):
    dataset_path = PROCESSED_DATA_DIR / category
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    train_loader, validation_loader, class_names, device = load_pytorch_datasets(
        dataset_path=dataset_path,
        batch_size=BATCH_SIZE,
    )

    model = build_resnet18_model(num_classes=len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

    mlflow.set_experiment("Industrial Defect Detection")

    with mlflow.start_run(run_name=f"pytorch_resnet18_{category}"):
        mlflow.log_param("framework", "PyTorch")
        mlflow.log_param("model", "ResNet18")
        mlflow.log_param("category", category)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("learning_rate", LEARNING_RATE)
        mlflow.log_param("batch_size", BATCH_SIZE)

        for epoch in range(EPOCHS):
            model.train()
            train_loss = 0.0
            correct = 0
            total = 0

            for images, labels in train_loader:
                images = images.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                outputs = model(images)
                loss = criterion(outputs, labels)

                loss.backward()
                optimizer.step()

                train_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            train_accuracy = correct / total
            avg_train_loss = train_loss / len(train_loader)

            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0

            with torch.no_grad():
                for images, labels in validation_loader:
                    images = images.to(device)
                    labels = labels.to(device)

                    outputs = model(images)
                    loss = criterion(outputs, labels)

                    val_loss += loss.item()

                    _, predicted = torch.max(outputs, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()

            val_accuracy = val_correct / val_total
            avg_val_loss = val_loss / len(validation_loader)

            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_accuracy, step=epoch)
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_accuracy, step=epoch)

            print(
                f"Epoch {epoch + 1}/{EPOCHS} "
                f"train_loss={avg_train_loss:.4f} "
                f"train_acc={train_accuracy:.4f} "
                f"val_loss={avg_val_loss:.4f} "
                f"val_acc={val_accuracy:.4f}"
            )

        model_path = MODEL_DIR / MODEL_FILENAME
        torch.save(model.state_dict(), model_path)

        mlflow.log_artifact(str(model_path))

        print(f"PyTorch model saved to: {model_path}")
