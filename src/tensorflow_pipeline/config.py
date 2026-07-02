"""
TensorFlow configuration for training.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

DEFAULT_CATEGORY = "bottle"

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 0.0001

RANDOM_SEED = 42

MODEL_NAME = "EfficientNetB0"

MODEL_FILENAME = "efficientnetb0_tf.keras"

NUM_CLASSES = 2

TRAIN_SPLIT = 0.8

VALIDATION_SPLIT = 0.2