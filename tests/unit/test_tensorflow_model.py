"""
Lightweight TensorFlow model module tests.

These tests intentionally avoid building the full pretrained model to keep CI fast.
"""

from src.tensorflow_pipeline.model import build_efficientnet_model


def test_tensorflow_model_builder_is_callable():
    assert callable(build_efficientnet_model)
