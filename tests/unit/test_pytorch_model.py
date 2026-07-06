"""
Lightweight PyTorch model module tests.

These tests intentionally avoid downloading pretrained weights in CI.
"""

from src.pytorch_pipeline.model import build_resnet18_model


def test_pytorch_model_builder_is_callable():
    assert callable(build_resnet18_model)
