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
from benchmarks.utils import (
    benchmark_metadata,
    summarize_latencies,
    time_function,
    write_csv,
    write_json,
)


def benchmark_get_endpoint(api_base_url: str, endpoint: str) -> tuple[dict, list[dict]]:
    url = f"{api_base_url}{endpoint}"

    for _ in range(WARMUP_REQUESTS):
        requests.get(url, timeout=30)

    raw_rows = []
    latencies = []

    for iteration in range(BENCHMARK_REQUESTS):
        latency_ms, response = time_function(lambda: requests.get(url, timeout=30))

        raw_rows.append(
            {
                "endpoint": endpoint,
                "method": "GET",
                "iteration": iteration + 1,
                "latency_ms": round(latency_ms, 2),
                "status_code": response.status_code,
            }
        )

        response.raise_for_status()
        latencies.append(latency_ms)

    summary = summarize_latencies(latencies)
    summary["endpoint"] = endpoint
    summary["method"] = "GET"

    return summary, raw_rows


def benchmark_predict_endpoint(
    api_base_url: str,
    image_path: Path,
    framework: str,
    category: str,
    model_version: str,
) -> tuple[dict, list[dict]]:
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

    raw_rows = []
    latencies = []

    for iteration in range(BENCHMARK_REQUESTS):
        with open(image_path, "rb") as image_file:
            latency_ms, response = time_function(
                lambda: requests.post(
                    url,
                    files={"file": (image_path.name, image_file, "image/png")},
                    data=data,
                    timeout=120,
                )
            )

        raw_rows.append(
            {
                "endpoint": "/predict",
                "method": "POST",
                "iteration": iteration + 1,
                "framework": framework,
                "category": category,
                "model_version": model_version,
                "latency_ms": round(latency_ms, 2),
                "status_code": response.status_code,
            }
        )

        response.raise_for_status()
        latencies.append(latency_ms)

    summary = summarize_latencies(latencies)
    summary["endpoint"] = "/predict"
    summary["method"] = "POST"
    summary["framework"] = framework
    summary["category"] = category
    summary["model_version"] = model_version

    return summary, raw_rows


def run_api_benchmarks(
    api_base_url: str,
    framework: str,
    category: str,
    model_version: str,
) -> list[dict]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    sample_image = create_sample_image(RESULTS_DIR / "sample.png")

    endpoint_summaries = []
    raw_results = []

    for endpoint in ["/", "/health", "/ready", "/metrics", "/cache", "/models"]:
        summary, raw_rows = benchmark_get_endpoint(api_base_url, endpoint)
        endpoint_summaries.append(summary)
        raw_results.extend(raw_rows)

    try:
        summary, raw_rows = benchmark_predict_endpoint(
            api_base_url=api_base_url,
            image_path=sample_image,
            framework=framework,
            category=category,
            model_version=model_version,
        )
        endpoint_summaries.append(summary)
        raw_results.extend(raw_rows)

    except requests.HTTPError as error:
        endpoint_summaries.append(
            {
                "endpoint": "/predict",
                "method": "POST",
                "framework": framework,
                "category": category,
                "model_version": model_version,
                "error": str(error),
            }
        )

    write_csv(RESULTS_DIR / "api_latency.csv", endpoint_summaries)
    write_csv(RESULTS_DIR / "api_raw_results.csv", raw_results)

    metadata = benchmark_metadata()
    metadata.update(
        {
            "api_base_url": api_base_url,
            "framework": framework,
            "category": category,
            "model_version": model_version,
            "warmup_requests": WARMUP_REQUESTS,
            "benchmark_requests": BENCHMARK_REQUESTS,
        }
    )
    write_json(RESULTS_DIR / "benchmark_metadata.json", metadata)

    print(f"API benchmark summary saved to: {RESULTS_DIR / 'api_latency.csv'}")
    print(f"API raw results saved to: {RESULTS_DIR / 'api_raw_results.csv'}")
    print(f"Benchmark metadata saved to: {RESULTS_DIR / 'benchmark_metadata.json'}")

    return endpoint_summaries


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
