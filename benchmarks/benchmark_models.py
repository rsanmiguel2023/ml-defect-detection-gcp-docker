"""
Benchmark local model loading and warm inference.

Usage:
    python -m benchmarks.benchmark_models --framework tensorflow --category bottle --model-version v1
"""

import argparse

from app.inference import predict_image
from benchmarks.config import (
    DEFAULT_CATEGORY,
    DEFAULT_FRAMEWORK,
    DEFAULT_MODEL_VERSION,
    RESULTS_DIR,
)
from benchmarks.create_sample_image import create_sample_image
from benchmarks.utils import summarize_latencies, time_function, write_csv


def benchmark_model_inference(
    framework: str,
    category: str,
    model_version: str,
    iterations: int,
) -> list[dict]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    sample_image_path = create_sample_image(RESULTS_DIR / "sample.png")
    image_bytes = sample_image_path.read_bytes()

    cold_latency_ms, _ = time_function(
        lambda: predict_image(
            image_bytes=image_bytes,
            framework=framework,
            category=category,
            model_version=model_version,
        )
    )

    warm_latencies = []
    for _ in range(iterations):
        latency_ms, _ = time_function(
            lambda: predict_image(
                image_bytes=image_bytes,
                framework=framework,
                category=category,
                model_version=model_version,
            )
        )
        warm_latencies.append(latency_ms)

    summary = summarize_latencies(warm_latencies)

    rows = [
        {
            "framework": framework,
            "category": category,
            "model_version": model_version,
            "metric": "cold_inference_ms",
            "value": round(cold_latency_ms, 2),
        },
        {
            "framework": framework,
            "category": category,
            "model_version": model_version,
            "metric": "warm_avg_ms",
            "value": summary["avg_ms"],
        },
        {
            "framework": framework,
            "category": category,
            "model_version": model_version,
            "metric": "warm_p95_ms",
            "value": summary["p95_ms"],
        },
    ]

    output_path = RESULTS_DIR / f"{framework}_model_latency.csv"
    write_csv(output_path, rows)
    print(f"Model benchmark results saved to: {output_path}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark local model inference")
    parser.add_argument("--framework", default=DEFAULT_FRAMEWORK)
    parser.add_argument("--category", default=DEFAULT_CATEGORY)
    parser.add_argument("--model-version", default=DEFAULT_MODEL_VERSION)
    parser.add_argument("--iterations", type=int, default=10)
    args = parser.parse_args()

    benchmark_model_inference(
        framework=args.framework,
        category=args.category,
        model_version=args.model_version,
        iterations=args.iterations,
    )


if __name__ == "__main__":
    main()
