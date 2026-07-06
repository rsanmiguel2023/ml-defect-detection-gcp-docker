"""
Benchmark configuration.
"""

from pathlib import Path

RESULTS_DIR = Path("results") / "benchmarks"

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_FRAMEWORK = "tensorflow"
DEFAULT_CATEGORY = "bottle"
DEFAULT_MODEL_VERSION = "latest"

WARMUP_REQUESTS = 3
BENCHMARK_REQUESTS = 20
BATCH_SIZES = [1, 5, 10, 25, 50]
