"""
Generate benchmark charts from CSV outputs.

Usage:
    python -m benchmarks.charts
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from benchmarks.config import RESULTS_DIR


def save_chart(output_base_path: Path) -> None:
    output_base_path.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_base_path.with_suffix(".png"), dpi=150)
    plt.savefig(output_base_path.with_suffix(".svg"))
    plt.close()


def plot_api_latency() -> None:
    path = RESULTS_DIR / "api_latency.csv"

    if not path.exists():
        return

    df = pd.read_csv(path)

    if "avg_ms" not in df.columns:
        return

    plt.figure(figsize=(10, 6))
    plt.bar(df["endpoint"], df["avg_ms"])
    plt.title("Average API Latency by Endpoint")
    plt.xlabel("Endpoint")
    plt.ylabel("Average Latency (ms)")
    plt.xticks(rotation=45, ha="right")

    save_chart(RESULTS_DIR / "api_latency")


def plot_batch_throughput() -> None:
    path = RESULTS_DIR / "batch_latency.csv"

    if not path.exists():
        return

    df = pd.read_csv(path)

    plt.figure(figsize=(10, 6))
    plt.plot(df["batch_size"], df["images_per_second"], marker="o")
    plt.title("Batch Prediction Throughput")
    plt.xlabel("Batch Size")
    plt.ylabel("Images per Second")

    save_chart(RESULTS_DIR / "batch_throughput")


def plot_framework_comparison() -> None:
    tensorflow_path = RESULTS_DIR / "tensorflow_model_latency.csv"
    pytorch_path = RESULTS_DIR / "pytorch_model_latency.csv"

    rows = []

    if tensorflow_path.exists():
        tensorflow_df = pd.read_csv(tensorflow_path)
        tensorflow_df["framework"] = "TensorFlow"
        rows.append(tensorflow_df)

    if pytorch_path.exists():
        pytorch_df = pd.read_csv(pytorch_path)
        pytorch_df["framework"] = "PyTorch"
        rows.append(pytorch_df)

    if not rows:
        return

    df = pd.concat(rows)

    warm_df = df[df["metric"].isin(["warm_avg_ms", "warm_p95_ms"])]

    if warm_df.empty:
        return

    pivot_df = warm_df.pivot(
        index="framework",
        columns="metric",
        values="value",
    )

    pivot_df.plot(kind="bar", figsize=(10, 6))

    plt.title("TensorFlow vs PyTorch Warm Inference Latency")
    plt.xlabel("Framework")
    plt.ylabel("Latency (ms)")
    plt.xticks(rotation=0)

    save_chart(RESULTS_DIR / "framework_comparison")


def plot_cold_vs_warm() -> None:
    tensorflow_path = RESULTS_DIR / "tensorflow_model_latency.csv"
    pytorch_path = RESULTS_DIR / "pytorch_model_latency.csv"

    rows = []

    if tensorflow_path.exists():
        tensorflow_df = pd.read_csv(tensorflow_path)
        tensorflow_df["framework"] = "TensorFlow"
        rows.append(tensorflow_df)

    if pytorch_path.exists():
        pytorch_df = pd.read_csv(pytorch_path)
        pytorch_df["framework"] = "PyTorch"
        rows.append(pytorch_df)

    if not rows:
        return

    df = pd.concat(rows)

    selected_df = df[df["metric"].isin(["cold_inference_ms", "warm_avg_ms"])]

    if selected_df.empty:
        return

    pivot_df = selected_df.pivot(
        index="framework",
        columns="metric",
        values="value",
    )

    pivot_df.plot(kind="bar", figsize=(10, 6))

    plt.title("Cold vs Warm Inference Latency")
    plt.xlabel("Framework")
    plt.ylabel("Latency (ms)")
    plt.xticks(rotation=0)

    save_chart(RESULTS_DIR / "cold_vs_warm")


def generate_charts() -> None:
    plot_api_latency()
    plot_batch_throughput()
    plot_framework_comparison()
    plot_cold_vs_warm()

    print(f"Benchmark charts saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    generate_charts()
