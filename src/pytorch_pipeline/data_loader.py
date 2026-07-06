"""
PyTorch dataset loader for processed MVTec AD category folders.
"""

from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def get_transforms():
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def load_pytorch_datasets(dataset_path: Path, batch_size: int = 32):
    train_dir = dataset_path / "train"
    validation_dir = dataset_path / "validation"

    transform = get_transforms()

    train_dataset = datasets.ImageFolder(
        root=train_dir,
        transform=transform,
    )

    validation_dataset = datasets.ImageFolder(
        root=validation_dir,
        transform=transform,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
    )

    class_names = train_dataset.classes

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    return train_loader, validation_loader, class_names, device
