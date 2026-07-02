"""
Generate model comparison report for TensorFlow and PyTorch results.
"""

import csv
from pathlib import Path

import pandas as pd

from src.common.config import REPORTS_DIR


def load_report(report_path: Path, framework: str):
    df = pd.read_csv(report_path)

    summary_rows = df[df["class"].isin(["macro avg", "weighted avg"])]

    records = []

    for _, row in summary_rows.iterrows():
        records.append(
            {
                "framework": framework,
                "average_type": row["class"],
                "precision": row["precision"],
                "recall": row["recall"],
                "f1_score": row["f1_score"],
                "support": row["support"],
            }
        )

    return records


def generate_model_comparison():
    tensorflow_report = REPORTS_DIR / "tensorflow_classification_report.csv"
    pytorch_report = REPORTS_DIR / "pytorch_classification_report.csv"

    records = []

    if tensorflow_report.exists():
        records.extend(load_report(tensorflow_report, "TensorFlow"))

    if pytorch_report.exists():
        records.extend(load_report(pytorch_report, "PyTorch"))

    output_path = REPORTS_DIR / "model_comparison.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "framework",
                "average_type",
                "precision",
                "recall",
                "f1_score",
                "support",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"Model comparison saved to: {output_path}")


if __name__ == "__main__":
    generate_model_comparison()
