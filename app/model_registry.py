"""
Model registry for loading and caching versioned TensorFlow and PyTorch models.
"""

import logging
from pathlib import Path

import tensorflow as tf
import torch

from app.config import DEFAULT_MODEL_VERSION, MODEL_ROOT
from src.pytorch_pipeline.model import build_resnet18_model

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Loads and caches ML models by framework, category, and version.
    """

    def __init__(self):
        self._cache = {}

    def _cache_key(self, framework: str, category: str, version: str) -> str:
        return f"{framework}:{category}:{version}"

    def _tensorflow_path(self, category: str, version: str) -> Path:
        return MODEL_ROOT / "tensorflow" / category / version / "model.keras"

    def _pytorch_path(self, category: str, version: str) -> Path:
        return MODEL_ROOT / "pytorch" / category / version / "model.pt"

    def load_tensorflow(
        self,
        category: str,
        version: str = DEFAULT_MODEL_VERSION,
    ):
        key = self._cache_key("tensorflow", category, version)

        if key not in self._cache:
            model_path = self._tensorflow_path(category, version)

            logger.info("Loading TensorFlow model from %s", model_path)

            self._cache[key] = tf.keras.models.load_model(model_path)

        return self._cache[key]

    def load_pytorch(
        self,
        category: str,
        version: str = DEFAULT_MODEL_VERSION,
    ):
        key = self._cache_key("pytorch", category, version)

        if key not in self._cache:
            model_path = self._pytorch_path(category, version)

            logger.info("Loading PyTorch model from %s", model_path)

            model = build_resnet18_model(num_classes=2)
            model.load_state_dict(torch.load(model_path, map_location="cpu"))
            model.eval()

            self._cache[key] = model

        return self._cache[key]


registry = ModelRegistry()
