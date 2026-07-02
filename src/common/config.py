"""
Shared project configuration.
"""

from pathlib import Path

# ------------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# ------------------------------------------------------------------
# Google Cloud Storage
# ------------------------------------------------------------------

GCP_PROJECT = "ml-defect-detection-rob"

GCS_BUCKET = "ml-defect-detection-rsanmiguel2023"

DATASET_PREFIX = "raw/mvtec_ad"

# ------------------------------------------------------------------
# Dataset
# ------------------------------------------------------------------

IMAGE_SIZE = (224, 224)

TRAIN_SPLIT = 0.70

VALIDATION_SPLIT = 0.15

TEST_SPLIT = 0.15

RANDOM_SEED = 42
