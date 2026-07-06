"""
Generate a Markdown performance report from benchmark CSV outputs.

Usage:
    python -m benchmarks.generate_report
"""

from pathlib import Path

import pandas as pd

from benchmarks.config import RESULTS_DIR


def read_csv_if_exists(path: Path):
    if path.exists():
        return pd.read_csv(path)
    return None


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "_No benchmark data available._"
    return df.to_markdown(index=False)


def generate_performance_report() -> Path:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    api_df = read_csv_if_exists(RESULTS_DIR / "api_latency.csv")
    batch_df = read_csv_if_exists(RESULTS_DIR / "batch_latency.csv")
    tensorflow_df = read_csv_if_exists(RESULTS_DIR / "tensorflow_model_latency.csv")
    pytorch_df = read_csv_if_exists(RESULTS_DIR / "pytorch_model_latency.csv")

    content = f"""# Performance Benchmarking

## Overview

This document summarizes benchmark results for the Industrial Defect Detection platform.

Benchmarks measure API latency, batch prediction throughput, and model inference performance.

---

## API Latency

{dataframe_to_markdown(api_df)}

---

## Batch Prediction Throughput

{dataframe_to_markdown(batch_df)}

---

## TensorFlow Model Inference

{dataframe_to_markdown(tensorflow_df)}

---

## PyTorch Model Inference

{dataframe_to_markdown(pytorch_df)}

---

## Notes

Benchmark results depend on:

- Local or cloud execution environment
- CPU and memory allocation
- Model cache state
- Cloud Run cold starts
- Network latency
- Batch size

Future improvements may include Prometheus metrics, Cloud Monitoring dashboards, and automated benchmark runs in CI.
"""

    output_path = docs_dir / "PERFORMANCE.md"
    output_path.write_text(content, encoding="utf-8")
    print(f"Performance report generated at: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_performance_report()
