"""
Unit tests for application configuration.
"""

from app.config import (
    DEFAULT_MODEL_VERSION,
    MODEL_ROOT,
    SUPPORTED_CATEGORIES,
    SUPPORTED_FRAMEWORKS,
)


def test_default_model_version():
    assert DEFAULT_MODEL_VERSION == "v1"


def test_supported_frameworks():
    assert "tensorflow" in SUPPORTED_FRAMEWORKS
    assert "pytorch" in SUPPORTED_FRAMEWORKS


def test_supported_categories_include_bottle():
    assert "bottle" in SUPPORTED_CATEGORIES


def test_model_root_is_models_directory():
    assert MODEL_ROOT.name == "models"
