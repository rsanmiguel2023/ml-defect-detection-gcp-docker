"""
Application configuration for inference service.
"""

from pathlib import Path

MODEL_ROOT = Path("models")

DEFAULT_MODEL_VERSION = "v1"

SUPPORTED_FRAMEWORKS = ["tensorflow", "pytorch"]

SUPPORTED_CATEGORIES = [
    "bottle",
    "cable",
    "capsule",
    "carpet",
    "grid",
    "hazelnut",
    "leather",
    "metal_nut",
    "pill",
    "screw",
    "tile",
    "toothbrush",
    "transistor",
    "wood",
    "zipper",
]
