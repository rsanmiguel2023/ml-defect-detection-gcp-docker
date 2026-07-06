"""
Report section builders for performance benchmark documentation.
"""

import json
from pathlib import Path

import fastapi
import pandas as pd
import tensorflow as tf
import torch

from benchmarks.config import RESULTS_DIR
from benchmarks.report_templates import (
    bullet_list,
    code_block,
    dataframe_to_markdown,
    heading,
    image,
    markdown_table,
    paragraph,
)


def read_csv_if_exists(path: Path) -> pd.DataFrame | None:
    if path.exists():
        return pd.read_csv(path)
    return None


def read_json_if_exists(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_value(
    df: pd.DataFrame | None, column: str, filter_column: str, filter_value: str
):
    if df is None or df.empty:
        return "N/A"

    if column not in df.columns or filter_column not in df.columns:
        return "N/A"

    filtered_df = df[df[filter_column] == filter_value]

    if filtered_df.empty:
        return "N/A"

    return filtered_df.iloc[0][column]


def safe_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def assess_latency(value) -> str:
    numeric_value = safe_float(value)

    if numeric_value is None:
        return "N/A"

    if numeric_value < 100:
        return "Excellent"

    if numeric_value < 200:
        return "Good"

    return "Needs optimization"


def assess_throughput(value) -> str:
    numeric_value = safe_float(value)

    if numeric_value is None:
        return "N/A"

    if numeric_value >= 20:
        return "Excellent"

    if numeric_value >= 10:
        return "Good"

    return "Needs optimization"


def load_benchmark_data() -> dict:
    return {
        "api": read_csv_if_exists(RESULTS_DIR / "api_latency.csv"),
        "api_raw": read_csv_if_exists(RESULTS_DIR / "api_raw_results.csv"),
        "batch": read_csv_if_exists(RESULTS_DIR / "batch_latency.csv"),
        "tensorflow": read_csv_if_exists(RESULTS_DIR / "tensorflow_model_latency.csv"),
        "pytorch": read_csv_if_exists(RESULTS_DIR / "pytorch_model_latency.csv"),
        "metadata": read_json_if_exists(RESULTS_DIR / "benchmark_metadata.json"),
    }


def executive_summary(data: dict) -> str:
    predict_avg = get_value(data["api"], "avg_ms", "endpoint", "/predict")
    tensorflow_warm = get_value(data["tensorflow"], "value", "metric", "warm_avg_ms")
    pytorch_warm = get_value(data["pytorch"], "value", "metric", "warm_avg_ms")

    return "\n\n".join(
        [
            heading("Executive Summary", 2),
            paragraph(
                """
                The Industrial Defect Detection platform was benchmarked to establish
                a repeatable performance baseline for API responsiveness, model
                inference latency, and batch prediction throughput.
                """
            ),
            paragraph(
                """
                The results in this report provide a reference for future optimization,
                capacity planning, and performance regression testing.
                """
            ),
            heading("Key Findings", 3),
            bullet_list(
                [
                    "Management endpoints responded with consistently low latency.",
                    f"Single-image prediction averaged approximately **{predict_avg} ms**.",
                    f"TensorFlow warm inference averaged approximately **{tensorflow_warm} ms**.",
                    f"PyTorch warm inference averaged approximately **{pytorch_warm} ms**.",
                    "Batch throughput improved as batch size increased.",
                    "Warm inference significantly outperformed cold inference.",
                ]
            ),
        ]
    )


def test_environment(data: dict) -> str:
    metadata = data["metadata"]

    rows = [
        ("Generated At", metadata.get("generated_at", "N/A")),
        ("Platform", metadata.get("platform", "N/A")),
        ("Python Version", metadata.get("python_version", "N/A")),
        ("TensorFlow Version", tf.__version__),
        ("PyTorch Version", torch.__version__),
        ("FastAPI Version", fastapi.__version__),
        ("Processor", metadata.get("processor", "N/A")),
        ("Git Commit", metadata.get("git_commit", "N/A")),
        ("API Base URL", metadata.get("api_base_url", "N/A")),
        ("Framework", metadata.get("framework", "N/A")),
        ("Category", metadata.get("category", "N/A")),
        ("Model Version", metadata.get("model_version", "N/A")),
        ("Warm-up Requests", metadata.get("warmup_requests", "N/A")),
        ("Benchmark Requests", metadata.get("benchmark_requests", "N/A")),
    ]

    return "\n\n".join([heading("Test Environment", 2), markdown_table(rows)])


def benchmark_methodology() -> str:
    return "\n\n".join(
        [
            heading("Benchmark Methodology", 2),
            paragraph(
                """
                The benchmark suite was executed using a controlled local testing
                approach. The objective was to establish a repeatable baseline for
                API, batch, and model inference performance.
                """
            ),
            bullet_list(
                [
                    "Warm-up requests were executed before measurement.",
                    "Latency was measured using Python's high-resolution `time.perf_counter()`.",
                    "Results include average, median, standard deviation, minimum, maximum, P50, P95, and P99 latency.",
                    "API benchmarks measured FastAPI endpoint response times.",
                    "Batch benchmarks measured throughput across multiple batch sizes.",
                    "Model benchmarks compared cold and warm inference behavior.",
                    "Benchmark outputs were exported as CSV files and summarized in this report.",
                ]
            ),
        ]
    )


def performance_assessment(data: dict) -> str:
    api_df = data["api"]
    batch_df = data["batch"]

    prediction_latency = get_value(api_df, "avg_ms", "endpoint", "/predict")
    tensorflow_warm = get_value(data["tensorflow"], "value", "metric", "warm_avg_ms")
    pytorch_warm = get_value(data["pytorch"], "value", "metric", "warm_avg_ms")

    batch_throughput = "N/A"
    if batch_df is not None and not batch_df.empty:
        batch_throughput = batch_df["images_per_second"].max()

    rows = [
        "| Metric | Result | Assessment |",
        "|---|---:|---|",
        (
            f"| API prediction latency | {prediction_latency} ms | "
            f"{assess_latency(prediction_latency)} |"
        ),
        (
            f"| TensorFlow warm inference | {tensorflow_warm} ms | "
            f"{assess_latency(tensorflow_warm)} |"
        ),
        (
            f"| PyTorch warm inference | {pytorch_warm} ms | "
            f"{assess_latency(pytorch_warm)} |"
        ),
        (
            f"| Batch throughput | {batch_throughput} images/sec | "
            f"{assess_throughput(batch_throughput)} |"
        ),
    ]

    return "\n\n".join(
        [
            heading("Performance Assessment", 2),
            paragraph(
                """
                The table below provides a simple assessment of the measured
                performance baseline. Thresholds are intended as project-level
                guidance and should be refined as production SLOs are defined.
                """
            ),
            "\n".join(rows),
        ]
    )


def summarized_api_table(api_df: pd.DataFrame | None) -> str:
    if api_df is None or api_df.empty:
        return "_No benchmark data available._"

    columns = [
        "endpoint",
        "method",
        "avg_ms",
        "p95_ms",
        "p99_ms",
        "requests_per_second",
    ]

    available_columns = [column for column in columns if column in api_df.columns]
    summary_df = api_df[available_columns].copy()

    return dataframe_to_markdown(summary_df)


def api_performance(data: dict) -> str:
    predict_avg = get_value(data["api"], "avg_ms", "endpoint", "/predict")

    return "\n\n".join(
        [
            heading("API Performance", 2),
            image(
                "../results/benchmarks/api_latency.png",
                "results/benchmarks/api_latency.png",
                "API Latency",
            ),
            heading("Analysis", 3),
            paragraph(
                """
                The benchmark results show that infrastructure endpoints such as
                `/health`, `/ready`, `/metrics`, `/cache`, and `/models` responded
                with low latency. These endpoints primarily validate application
                state and metadata, so they introduce minimal processing overhead.
                """
            ),
            paragraph(
                f"""
                The `/predict` endpoint averaged approximately **{predict_avg} ms**
                because the request lifecycle includes file upload handling, image
                preprocessing, model lookup, inference execution, and response
                serialization.
                """
            ),
            heading("Measured API Performance", 3),
            summarized_api_table(data["api"]),
            paragraph(
                """
                Detailed raw API benchmark results are retained in
                `results/benchmarks/api_latency.csv` and
                `results/benchmarks/api_raw_results.csv`.
                """
            ),
        ]
    )


def batch_performance(data: dict) -> str:
    batch_df = data["batch"]

    first_throughput = "N/A"
    max_throughput = "N/A"

    if batch_df is not None and not batch_df.empty:
        first_throughput = batch_df.iloc[0]["images_per_second"]
        max_throughput = batch_df["images_per_second"].max()

    return "\n\n".join(
        [
            heading("Batch Prediction Performance", 2),
            image(
                "../results/benchmarks/batch_throughput.png",
                "results/benchmarks/batch_throughput.png",
                "Batch Throughput",
            ),
            heading("Analysis", 3),
            paragraph(
                f"""
                Batch throughput increased from approximately **{first_throughput}
                images/second** on the smallest batch to approximately
                **{max_throughput} images/second** at the highest measured throughput.
                Request overhead, preprocessing overhead, and model execution overhead
                are amortized across larger batches.
                """
            ),
            paragraph(
                """
                In production, the best batch size depends on latency requirements,
                memory allocation, CPU allocation, and workload concurrency.
                """
            ),
            heading("Batch Results", 3),
            dataframe_to_markdown(batch_df),
        ]
    )


def model_performance(data: dict) -> str:
    return "\n\n".join(
        [
            heading("Model Performance", 2),
            heading("TensorFlow Model Performance", 3),
            paragraph(
                """
                TensorFlow results include cold inference and warm inference. Cold
                inference includes model loading and initialization effects, while
                warm inference reflects repeated predictions after the model has
                already been loaded and cached.
                """
            ),
            dataframe_to_markdown(data["tensorflow"]),
            heading("PyTorch Model Performance", 3),
            paragraph(
                """
                PyTorch results include cold inference and warm inference for the
                ResNet18 pipeline. These measurements are specific to the model
                architecture, hardware, software versions, and local runtime
                configuration.
                """
            ),
            dataframe_to_markdown(data["pytorch"]),
        ]
    )


def framework_comparison(data: dict) -> str:
    tensorflow_df = data["tensorflow"]
    pytorch_df = data["pytorch"]

    rows = [
        (
            "Cold inference",
            get_value(tensorflow_df, "value", "metric", "cold_inference_ms"),
            get_value(pytorch_df, "value", "metric", "cold_inference_ms"),
        ),
        (
            "Warm average",
            get_value(tensorflow_df, "value", "metric", "warm_avg_ms"),
            get_value(pytorch_df, "value", "metric", "warm_avg_ms"),
        ),
        (
            "Warm P95",
            get_value(tensorflow_df, "value", "metric", "warm_p95_ms"),
            get_value(pytorch_df, "value", "metric", "warm_p95_ms"),
        ),
    ]

    comparison_table = [
        "| Metric | TensorFlow ms | PyTorch ms |",
        "|---|---:|---:|",
    ]

    for metric, tensorflow_value, pytorch_value in rows:
        comparison_table.append(f"| {metric} | {tensorflow_value} | {pytorch_value} |")

    return "\n\n".join(
        [
            heading("Framework Comparison", 2),
            image(
                "../results/benchmarks/framework_comparison.png",
                "results/benchmarks/framework_comparison.png",
                "Framework Comparison",
            ),
            image(
                "../results/benchmarks/cold_vs_warm.png",
                "results/benchmarks/cold_vs_warm.png",
                "Cold vs Warm Inference",
            ),
            heading("Comparison Table", 3),
            "\n".join(comparison_table),
            heading("Analysis", 3),
            paragraph(
                """
                In this benchmark environment, the PyTorch implementation produced
                lower cold-start and warm inference latency than the TensorFlow
                implementation.
                """
            ),
            paragraph(
                """
                These observations are specific to the evaluated models, preprocessing
                pipeline, runtime configuration, and hardware platform, and should not
                be interpreted as a general comparison between frameworks.
                """
            ),
        ]
    )


def performance_baseline() -> str:
    return "\n\n".join(
        [
            heading("Performance Baseline", 2),
            paragraph(
                """
                The measurements presented in this report represent the baseline
                performance for the current implementation. Future benchmark runs
                should compare against these results to identify regressions,
                validate optimizations, and support capacity planning.
                """
            ),
        ]
    )


def recommendations() -> str:
    return "\n\n".join(
        [
            heading("Recommendations", 2),
            heading("Short-term", 3),
            bullet_list(
                [
                    "Monitor P95 and P99 latency in production.",
                    "Profile image preprocessing to reduce single-image prediction latency.",
                    "Compare local benchmark results against Cloud Run execution.",
                ]
            ),
            heading("Medium-term", 3),
            bullet_list(
                [
                    "Use Cloud Run minimum instances if cold-start latency becomes a concern.",
                    "Tune Cloud Run CPU and memory allocation for inference-heavy workloads.",
                    "Extend benchmarks across all MVTec AD categories.",
                ]
            ),
            heading("Long-term", 3),
            bullet_list(
                [
                    "Add automated benchmark runs before major releases.",
                    "Introduce load testing with concurrent users.",
                    "Evaluate GPU-backed inference for higher-throughput workloads.",
                ]
            ),
        ]
    )


def conclusions() -> str:
    return "\n\n".join(
        [
            heading("Conclusions", 2),
            paragraph(
                """
                The benchmark suite successfully established a repeatable baseline
                for API latency, batch throughput, and model inference performance.
                """
            ),
            bullet_list(
                [
                    "API management endpoints consistently returned low-latency responses.",
                    "Prediction latency is primarily driven by preprocessing and model inference.",
                    "Batch prediction improved throughput at larger batch sizes.",
                    "Warm inference substantially reduced latency compared with cold inference.",
                    "The results provide a baseline for future performance optimization and regression testing.",
                ]
            ),
        ]
    )


def limitations() -> str:
    return "\n\n".join(
        [
            heading("Limitations", 2),
            bullet_list(
                [
                    "Benchmarks were executed in a local development environment.",
                    "Synthetic sample images were used for lightweight benchmark execution.",
                    "GPU acceleration was not evaluated.",
                    "Production network latency was not fully measured.",
                    "Results may vary depending on hardware, model cache state, and runtime configuration.",
                ]
            ),
        ]
    )


def future_enhancements() -> str:
    return "\n\n".join(
        [
            heading("Future Enhancements", 2),
            bullet_list(
                [
                    "Cloud Run benchmark execution.",
                    "Prometheus-compatible metrics.",
                    "Google Cloud Monitoring dashboards.",
                    "Load testing with concurrent users.",
                    "GPU-backed inference benchmarks.",
                    "Memory and CPU profiling.",
                    "Automated performance regression checks in CI.",
                    "Automatically publish benchmark reports as GitHub Actions artifacts.",
                    "Compare benchmark results across Git commits to detect regressions.",
                    "Portfolio-ready benchmark dashboard.",
                ]
            ),
        ]
    )


def benchmark_metadata(data: dict) -> str:
    metadata = data["metadata"]

    rows = [
        ("Git Commit", metadata.get("git_commit", "N/A")),
        ("Generated At", metadata.get("generated_at", "N/A")),
        ("Environment", "Local Development"),
        ("Operating System", metadata.get("platform", "N/A")),
        ("CPU", metadata.get("processor", "N/A")),
        ("API Base URL", metadata.get("api_base_url", "N/A")),
        ("Framework", metadata.get("framework", "N/A")),
        ("Category", metadata.get("category", "N/A")),
        ("Model Version", metadata.get("model_version", "N/A")),
    ]

    return "\n\n".join([heading("Benchmark Metadata", 2), markdown_table(rows)])


def generated_artifacts() -> str:
    return "\n\n".join(
        [
            heading("Generated Artifacts", 2),
            paragraph("Benchmark outputs are stored in:"),
            code_block("results/benchmarks/"),
            paragraph("Expected artifacts include:"),
            code_block(
                """
docs/PERFORMANCE.md
api_latency.csv
api_raw_results.csv
batch_latency.csv
tensorflow_model_latency.csv
pytorch_model_latency.csv
benchmark_metadata.json
api_latency.png
api_latency.svg
batch_throughput.png
batch_throughput.svg
framework_comparison.png
framework_comparison.svg
cold_vs_warm.png
cold_vs_warm.svg
                """
            ),
        ]
    )
