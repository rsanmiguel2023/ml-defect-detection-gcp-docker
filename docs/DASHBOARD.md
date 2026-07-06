# Operations Dashboard

## Overview

This document defines the recommended production dashboard layout for the Industrial Defect Detection platform.

The dashboard should provide a single operational view of API health, prediction performance, model behavior, infrastructure usage, and deployment status.

## Dashboard Goals

The dashboard should help operators answer:

- Is the API healthy?
- Are predictions succeeding?
- Is latency within target?
- Are models loading correctly?
- Is Cloud Run under resource pressure?
- Did a recent deployment cause degradation?
- Are batch workloads performing as expected?

## Dashboard Sections

### 1. Service Health

| Widget | Metric | Purpose |
|---|---|---|
| API Availability | 2xx / total requests | Tracks service availability |
| Error Rate | 5xx / total requests | Detects application failure |
| Health Check Latency | P95 `/health` latency | Validates process responsiveness |
| Readiness Latency | P95 `/ready` latency | Validates readiness to serve traffic |

### 2. Prediction Performance

| Widget | Metric | Purpose |
|---|---|---|
| Predict Latency P50 | Median `/predict` latency | Typical user experience |
| Predict Latency P95 | P95 `/predict` latency | SLO tracking |
| Predict Latency P99 | P99 `/predict` latency | Tail latency detection |
| Prediction Count | Number of predictions | Usage tracking |
| Prediction Errors | Failed predictions | Model or request issues |

### 3. Model Observability

| Widget | Metric | Purpose |
|---|---|---|
| Predictions by Framework | TensorFlow vs PyTorch | Framework usage |
| Predictions by Category | MVTec category count | Workload distribution |
| Predictions by Model Version | Version usage | Version tracking |
| Model Load Failures | Failed model load events | Registry issues |
| Cache Hit Rate | cache hits / lookups | Model serving efficiency |

### 4. Batch Performance

| Widget | Metric | Purpose |
|---|---|---|
| Batch Request Count | Batch endpoint traffic | Batch workload tracking |
| Batch Latency P95 | P95 `/predict-batch` latency | Batch SLO monitoring |
| Images per Second | Batch throughput | Capacity measurement |
| Batch Size Distribution | Batch sizes submitted | Usage pattern analysis |

### 5. Cloud Run Runtime

| Widget | Metric | Purpose |
|---|---|---|
| CPU Utilization | Container CPU usage | Capacity and scaling |
| Memory Utilization | Container memory usage | OOM prevention |
| Instance Count | Active Cloud Run instances | Scaling visibility |
| Cold Starts | Container startup count | Startup impact tracking |
| Container Restarts | Restart events | Runtime stability |

### 6. Deployment and CI/CD

| Widget | Metric | Purpose |
|---|---|---|
| Last Deployment Status | GitHub Actions result | Release visibility |
| Deployment Frequency | Deploys per week | Delivery tracking |
| Failed Deployments | Failed CI/CD runs | Release risk |
| Active Image Tag | Artifact Registry image | Runtime traceability |

## Example Dashboard Layout

```text
+-------------------------------------------------------------+
| Service Health                                              |
| Availability | Error Rate | Health P95 | Ready P95          |
+-------------------------------------------------------------+
| Prediction Performance                                      |
| P50 Latency | P95 Latency | P99 Latency | Prediction Count   |
+-------------------------------------------------------------+
| Model Observability                                         |
| Framework Usage | Category Usage | Cache Hit Rate          |
+-------------------------------------------------------------+
| Batch Performance                                           |
| Batch Latency | Images/sec | Batch Size Distribution       |
+-------------------------------------------------------------+
| Cloud Run Runtime                                           |
| CPU | Memory | Instances | Cold Starts | Restarts           |
+-------------------------------------------------------------+
| Deployment                                                  |
| Last Deploy | Failed Deploys | Active Image Tag              |
+-------------------------------------------------------------+
```

## Future Enhancements

- Google Cloud Monitoring dashboard JSON export.
- Grafana dashboard version.
- Automated dashboard screenshots for documentation.
- Per-model and per-category dashboards.
- SLO burn-rate panels.
