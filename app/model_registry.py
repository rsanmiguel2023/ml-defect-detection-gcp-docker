"""
Model registry for loading, caching, and resolving versioned ML models.
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
        self.cache_hits = 0
        self.cache_misses = 0

    def _cache_key(self, framework: str, category: str, version: str) -> str:
        return f"{framework}:{category}:{version}"

    def _model_dir(self, framework: str, category: str) -> Path:
        return MODEL_ROOT / framework / category

    def list_versions(self, framework: str, category: str) -> list[str]:
        model_dir = self._model_dir(framework, category)

        if not model_dir.exists():
            return []

        return sorted([path.name for path in model_dir.iterdir() if path.is_dir()])

    def resolve_version(
        self,
        framework: str,
        category: str,
        version: str = DEFAULT_MODEL_VERSION,
    ) -> str:
        versions = self.list_versions(framework, category)

        if not versions:
            raise FileNotFoundError(
                f"No model versions found for {framework}/{category}"
            )

        if version == "latest":
            return versions[-1]

        if version not in versions:
            raise FileNotFoundError(
                f"Model version '{version}' not found for {framework}/{category}"
            )

        return version

    def _tensorflow_path(self, category: str, version: str) -> Path:
        return MODEL_ROOT / "tensorflow" / category / version / "model.keras"

    def _pytorch_path(self, category: str, version: str) -> Path:
        return MODEL_ROOT / "pytorch" / category / version / "model.pt"

    def load_tensorflow(
        self,
        category: str,
        version: str = DEFAULT_MODEL_VERSION,
    ):
        resolved_version = self.resolve_version("tensorflow", category, version)
        key = self._cache_key("tensorflow", category, resolved_version)

        if key in self._cache:
            self.cache_hits += 1
            return self._cache[key]

        self.cache_misses += 1
        model_path = self._tensorflow_path(category, resolved_version)
        logger.info("Loading TensorFlow model from %s", model_path)

        self._cache[key] = tf.keras.models.load_model(model_path)
        return self._cache[key]

    def load_pytorch(
        self,
        category: str,
        version: str = DEFAULT_MODEL_VERSION,
    ):
        resolved_version = self.resolve_version("pytorch", category, version)
        key = self._cache_key("pytorch", category, resolved_version)

        if key in self._cache:
            self.cache_hits += 1
            return self._cache[key]

        self.cache_misses += 1
        model_path = self._pytorch_path(category, resolved_version)
        logger.info("Loading PyTorch model from %s", model_path)

        model = build_resnet18_model(num_classes=2)
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()

        self._cache[key] = model
        return self._cache[key]

    def cache_stats(self) -> dict:
        return {
            "cached_models": len(self._cache),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_keys": list(self._cache.keys()),
        }


registry = ModelRegistry()
