# Performance Benchmarking

## Overview

This document summarizes benchmark results for the Industrial Defect Detection platform.

Benchmarks measure API latency, batch prediction throughput, and model inference performance.

---

## API Latency

|   avg_ms | category   |   count | endpoint   | framework   |   max_ms |   median_ms | method   |   min_ms | model_version   |   p50_ms |   p95_ms |   p99_ms |   requests_per_second |   stdev_ms |
|---------:|:-----------|--------:|:-----------|:------------|---------:|------------:|:---------|---------:|:----------------|---------:|---------:|---------:|----------------------:|-----------:|
|    11.21 | nan        |      20 | /          | nan         |    16.02 |       15.09 | GET      |     1.65 | nan             |    15.14 |    15.98 |    16.02 |                 89.18 |       6.27 |
|    13.31 | nan        |      20 | /health    | nan         |    27.29 |       15.42 | GET      |     1.75 | nan             |    15.46 |    15.91 |    27.29 |                 75.13 |       6.46 |
|    10.58 | nan        |      20 | /ready     | nan         |    26.35 |       14.37 | GET      |     1.68 | nan             |    14.64 |    22.7  |    26.35 |                 94.55 |       8.56 |
|    14.24 | nan        |      20 | /metrics   | nan         |    16.62 |       15.34 | GET      |     1.78 | nan             |    15.39 |    16.32 |    16.62 |                 70.25 |       4    |
|    13.53 | nan        |      20 | /cache     | nan         |    16.13 |       15.49 | GET      |     1.98 | nan             |    15.51 |    15.99 |    16.13 |                 73.9  |       4.8  |
|    14.74 | nan        |      20 | /models    | nan         |    16.41 |       15.48 | GET      |     2.48 | nan             |    15.53 |    16.3  |    16.41 |                 67.83 |       2.98 |
|    76.1  | bottle     |      20 | /predict   | tensorflow  |    86.49 |       76.8  | POST     |    58.61 | latest          |    77.3  |    85.7  |    86.49 |                 13.14 |       6.94 |

---

## Batch Prediction Throughput

|   batch_size | category   | framework   |   images_per_second |   latency_ms | model_version   |   status_code |
|-------------:|:-----------|:------------|--------------------:|-------------:|:----------------|--------------:|
|            1 | bottle     | tensorflow  |                0.59 |      1685.2  | latest          |           200 |
|            5 | bottle     | tensorflow  |               17.06 |       293.12 | latest          |           200 |
|           10 | bottle     | tensorflow  |               18.22 |       548.8  | latest          |           200 |
|           25 | bottle     | tensorflow  |               18.9  |      1322.81 | latest          |           200 |
|           50 | bottle     | tensorflow  |               19.32 |      2588.11 | latest          |           200 |

---

## TensorFlow Model Inference

| category   | framework   | metric            | model_version   |   value |
|:-----------|:------------|:------------------|:----------------|--------:|
| bottle     | tensorflow  | cold_inference_ms | v1              | 1544.23 |
| bottle     | tensorflow  | warm_avg_ms       | v1              |   58.94 |
| bottle     | tensorflow  | warm_p95_ms       | v1              |   65.97 |

---

## PyTorch Model Inference

| category   | framework   | metric            | model_version   |   value |
|:-----------|:------------|:------------------|:----------------|--------:|
| bottle     | pytorch     | cold_inference_ms | v1              |  369.19 |
| bottle     | pytorch     | warm_avg_ms       | v1              |   10.81 |
| bottle     | pytorch     | warm_p95_ms       | v1              |   13.1  |

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
