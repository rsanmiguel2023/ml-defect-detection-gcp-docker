"""
Benchmark FastAPI endpoints.

Usage:
    python -m benchmarks.benchmark_api
"""

import argparse
from pathlib import Path

import requests

from benchmarks.config import (
    BENCHMARK_REQUESTS,
    DEFAULT_API_BASE_URL,
    DEFAULT_CATEGORY,
    DEFAULT_FRAMEWORK,
    DEFAULT_MODEL_VERSION,
    RESULTS_DIR,
    WARMUP_REQUESTS,
)
from benchmarks.create_sample_image import create_sample_image
from benchmarks.utils import summarize_latencies, time_function, write_csv


def benchmark_get_endpoint(api_base_url: str, endpoint: str) -> dict:
    url = f"{api_base_url}{endpoint}"

    for _ in range(WARMUP_REQUESTS):
        requests.get(url, timeout=30)

    latencies = []
    for _ in range(BENCHMARK_REQUESTS):
        latency_ms, response = time_function(lambda: requests.get(url, timeout=30))
        response.raise_for_status()
        latencies.append(latency_ms)

    summary = summarize_latencies(latencies)
    summary["endpoint"] = endpoint
    summary["method"] = "GET"
    return summary


def benchmark_predict_endpoint(
    api_base_url: str,
    image_path: Path,
    framework: str,
    category: str,
    model_version: str,
) -> dict:
    url = f"{api_base_url}/predict"
    data = {
        "framework": framework,
        "category": category,
        "model_version": model_version,
    }

    for _ in range(WARMUP_REQUESTS):
        with open(image_path, "rb") as image_file:
            response = requests.post(
                url,
                files={"file": (image_path.name, image_file, "image/png")},
                data=data,
                timeout=120,
            )
        response.raise_for_status()

    latencies = []
    for _ in range(BENCHMARK_REQUESTS):
        with open(image_path, "rb") as image_file:
            latency_ms, response = time_function(
                lambda: requests.post(
                    url,
                    files={"file": (image_path.name, image_file, "image/png")},
                    data=data,
                    timeout=120,
                )
            )
        response.raise_for_status()
        latencies.append(latency_ms)

    summary = summarize_latencies(latencies)
    summary["endpoint"] = "/predict"
    summary["method"] = "POST"
    summary["framework"] = framework
    summary["category"] = category
    summary["model_version"] = model_version
    return summary


def run_api_benchmarks(
    api_base_url: str,
    framework: str,
    category: str,
    model_version: str,
) -> list[dict]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sample_image = create_sample_image(RESULTS_DIR / "sample.png")

    rows = [
        benchmark_get_endpoint(api_base_url, "/health"),
        benchmark_get_endpoint(api_base_url, "/ready"),
        benchmark_get_endpoint(api_base_url, "/metrics"),
        benchmark_get_endpoint(api_base_url, "/models"),
    ]

    try:
        rows.append(
            benchmark_predict_endpoint(
                api_base_url=api_base_url,
                image_path=sample_image,
                framework=framework,
                category=category,
                model_version=model_version,
            )
        )
    except requests.HTTPError as error:
        rows.append(
            {
                "endpoint": "/predict",
                "method": "POST",
                "framework": framework,
                "category": category,
                "model_version": model_version,
                "error": str(error),
            }
        )

    output_path = RESULTS_DIR / "api_latency.csv"
    write_csv(output_path, rows)
    print(f"API benchmark results saved to: {output_path}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark FastAPI endpoints")
    parser.add_argument("--api-base-url", default=DEFAULT_API_BASE_URL)
    parser.add_argument("--framework", default=DEFAULT_FRAMEWORK)
    parser.add_argument("--category", default=DEFAULT_CATEGORY)
    parser.add_argument("--model-version", default=DEFAULT_MODEL_VERSION)
    args = parser.parse_args()

    run_api_benchmarks(
        api_base_url=args.api_base_url,
        framework=args.framework,
        category=args.category,
        model_version=args.model_version,
    )


if __name__ == "__main__":
    main()
