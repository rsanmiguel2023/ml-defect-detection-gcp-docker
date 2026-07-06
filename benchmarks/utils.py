"""
Shared benchmark utilities.
"""

import csv
import json
import platform
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def percentile(values: list[float], percentile_rank: float) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = int(round((percentile_rank / 100) * (len(sorted_values) - 1)))

    return sorted_values[index]


def summarize_latencies(latencies_ms: list[float]) -> dict:
    if not latencies_ms:
        return {
            "count": 0,
            "avg_ms": 0.0,
            "median_ms": 0.0,
            "stdev_ms": 0.0,
            "min_ms": 0.0,
            "max_ms": 0.0,
            "p50_ms": 0.0,
            "p95_ms": 0.0,
            "p99_ms": 0.0,
            "requests_per_second": 0.0,
        }

    total_seconds = sum(latencies_ms) / 1000

    return {
        "count": len(latencies_ms),
        "avg_ms": round(statistics.mean(latencies_ms), 2),
        "median_ms": round(statistics.median(latencies_ms), 2),
        "stdev_ms": (
            round(statistics.stdev(latencies_ms), 2) if len(latencies_ms) > 1 else 0.0
        ),
        "min_ms": round(min(latencies_ms), 2),
        "max_ms": round(max(latencies_ms), 2),
        "p50_ms": round(percentile(latencies_ms, 50), 2),
        "p95_ms": round(percentile(latencies_ms, 95), 2),
        "p99_ms": round(percentile(latencies_ms, 99), 2),
        "requests_per_second": (
            round(len(latencies_ms) / total_seconds, 2) if total_seconds > 0 else 0.0
        ),
    }


def time_function(function: Callable) -> tuple[float, object]:
    start_time = time.perf_counter()
    result = function()
    latency_ms = (time.perf_counter() - start_time) * 1000

    return latency_ms, result


def write_csv(path: Path, rows: list[dict]) -> None:
    ensure_directory(path.parent)

    if not rows:
        return

    fieldnames = sorted({key for row in rows for key in row.keys()})

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    ensure_directory(path.parent)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def get_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def benchmark_metadata() -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "git_commit": get_git_commit(),
    }
