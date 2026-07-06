"""
Benchmark batch prediction endpoint.

Usage:
    python -m benchmarks.benchmark_batch
"""

import argparse
from pathlib import Path

import requests

from benchmarks.config import (
    BATCH_SIZES,
    DEFAULT_API_BASE_URL,
    DEFAULT_CATEGORY,
    DEFAULT_FRAMEWORK,
    DEFAULT_MODEL_VERSION,
    RESULTS_DIR,
)
from benchmarks.create_sample_image import create_sample_image
from benchmarks.utils import benchmark_metadata, time_function, write_csv, write_json


def benchmark_batch_prediction(
    api_base_url: str,
    image_path: Path,
    framework: str,
    category: str,
    model_version: str,
) -> list[dict]:
    url = f"{api_base_url}/predict-batch"

    rows = []

    for batch_size in BATCH_SIZES:
        files = [
            (
                "files",
                (
                    f"sample_{index}.png",
                    image_path.read_bytes(),
                    "image/png",
                ),
            )
            for index in range(batch_size)
        ]

        data = {
            "framework": framework,
            "category": category,
            "model_version": model_version,
        }

        latency_ms, response = time_function(
            lambda: requests.post(
                url,
                files=files,
                data=data,
                timeout=300,
            )
        )

        response.raise_for_status()

        rows.append(
            {
                "batch_size": batch_size,
                "framework": framework,
                "category": category,
                "model_version": model_version,
                "latency_ms": round(latency_ms, 2),
                "images_per_second": round(batch_size / (latency_ms / 1000), 2),
                "status_code": response.status_code,
            }
        )

    output_path = RESULTS_DIR / "batch_latency.csv"
    write_csv(output_path, rows)

    metadata = benchmark_metadata()
    metadata.update(
        {
            "api_base_url": api_base_url,
            "framework": framework,
            "category": category,
            "model_version": model_version,
            "batch_sizes": BATCH_SIZES,
        }
    )
    write_json(RESULTS_DIR / "batch_benchmark_metadata.json", metadata)

    print(f"Batch benchmark results saved to: {output_path}")
    print(
        "Batch benchmark metadata saved to: "
        f"{RESULTS_DIR / 'batch_benchmark_metadata.json'}"
    )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark batch prediction endpoint")

    parser.add_argument("--api-base-url", default=DEFAULT_API_BASE_URL)
    parser.add_argument("--framework", default=DEFAULT_FRAMEWORK)
    parser.add_argument("--category", default=DEFAULT_CATEGORY)
    parser.add_argument("--model-version", default=DEFAULT_MODEL_VERSION)

    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sample_image = create_sample_image(RESULTS_DIR / "sample.png")

    benchmark_batch_prediction(
        api_base_url=args.api_base_url,
        image_path=sample_image,
        framework=args.framework,
        category=args.category,
        model_version=args.model_version,
    )


if __name__ == "__main__":
    main()
