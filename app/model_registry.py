"""
Model registry for loading and caching TensorFlow and PyTorch models.
"""

from pathlib import Path

import tensorflow as tf
import torch

from src.pytorch_pipeline.model import build_resnet18_model

MODEL_DIR = Path("models")


class ModelRegistry:
    """
    Loads and caches ML models.
    """

    def __init__(self):
        self._tensorflow_models = {}
        self._pytorch_models = {}

    def load_tensorflow(self, category: str):
        if category not in self._tensorflow_models:

            model_path = MODEL_DIR / "efficientnetb0_tf.keras"

            self._tensorflow_models[category] = tf.keras.models.load_model(model_path)

        return self._tensorflow_models[category]

    def load_pytorch(self, category: str):

        if category not in self._pytorch_models:

            model = build_resnet18_model(num_classes=2)

            model.load_state_dict(
                torch.load(
                    MODEL_DIR / "resnet18_pytorch.pt",
                    map_location="cpu",
                )
            )

            model.eval()

            self._pytorch_models[category] = model

        return self._pytorch_models[category]


registry = ModelRegistry()
