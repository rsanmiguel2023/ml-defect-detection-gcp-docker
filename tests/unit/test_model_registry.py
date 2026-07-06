"""
Unit tests for versioned model registry behavior.
"""

import pytest

from app import model_registry
from app.model_registry import ModelRegistry


def test_list_versions_returns_empty_for_missing_model_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(model_registry, "MODEL_ROOT", tmp_path)

    registry = ModelRegistry()

    versions = registry.list_versions("tensorflow", "bottle")

    assert versions == []


def test_list_versions_returns_sorted_versions(tmp_path, monkeypatch):
    monkeypatch.setattr(model_registry, "MODEL_ROOT", tmp_path)

    model_dir = tmp_path / "tensorflow" / "bottle"
    (model_dir / "v2").mkdir(parents=True)
    (model_dir / "v1").mkdir(parents=True)

    registry = ModelRegistry()

    versions = registry.list_versions("tensorflow", "bottle")

    assert versions == ["v1", "v2"]


def test_resolve_latest_version(tmp_path, monkeypatch):
    monkeypatch.setattr(model_registry, "MODEL_ROOT", tmp_path)

    model_dir = tmp_path / "tensorflow" / "bottle"
    (model_dir / "v1").mkdir(parents=True)
    (model_dir / "v2").mkdir(parents=True)

    registry = ModelRegistry()

    resolved = registry.resolve_version("tensorflow", "bottle", "latest")

    assert resolved == "v2"


def test_resolve_missing_version_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(model_registry, "MODEL_ROOT", tmp_path)

    model_dir = tmp_path / "tensorflow" / "bottle"
    (model_dir / "v1").mkdir(parents=True)

    registry = ModelRegistry()

    with pytest.raises(FileNotFoundError):
        registry.resolve_version("tensorflow", "bottle", "v99")


def test_cache_stats_initial_state():
    registry = ModelRegistry()

    stats = registry.cache_stats()

    assert stats["cached_models"] == 0
    assert stats["cache_hits"] == 0
    assert stats["cache_misses"] == 0
    assert stats["cache_keys"] == []
