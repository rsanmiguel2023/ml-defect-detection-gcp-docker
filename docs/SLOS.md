# Service Level Objectives and Indicators

## Overview

This document defines the Service Level Indicators (SLIs), Service Level Objectives (SLOs), and operational targets for the Industrial Defect Detection platform.

The goal is to establish measurable reliability and performance expectations for the FastAPI inference service, model prediction endpoints, and supporting platform components.

## Service Scope

The monitored service includes:

- FastAPI inference API
- TensorFlow prediction endpoint
- PyTorch prediction endpoint
- Batch prediction endpoint
- Model registry
- Cloud Run runtime
- Artifact Registry image source
- Cloud Storage model and data dependencies

## Service Level Indicators

| SLI | Description | Measurement |
|---|---|---|
| Availability | Percentage of successful API responses | HTTP 2xx / total requests |
| Error Rate | Percentage of failed requests | HTTP 5xx / total requests |
| Prediction Latency | Time to complete single-image inference | P50, P95, P99 latency |
| Batch Throughput | Images processed per second | Images/sec |
| Health Latency | Time to respond to `/health` | P95 latency |
| Readiness Latency | Time to respond to `/ready` | P95 latency |
| Model Load Success | Successful model load operations | Success/failure logs |
| Cache Hit Rate | Percentage of model requests served from cache | cache hits / total cache lookups |
| Cold Start Duration | Time for service to become responsive after startup | startup latency |
| Deployment Success | Successful Cloud Run deployments | CI/CD deployment status |

## Service Level Objectives

| Objective | Target |
|---|---:|
| API Availability | 99.9% monthly |
| API Error Rate | < 1% monthly |
| P95 `/predict` Latency | < 150 ms |
| P99 `/predict` Latency | < 300 ms |
| P95 `/health` Latency | < 25 ms |
| P95 `/ready` Latency | < 25 ms |
| Batch Throughput | > 15 images/sec |
| Model Cache Hit Rate | > 90% after warm-up |
| Deployment Success Rate | > 95% |
| Cold Start Duration | < 3 seconds |

## Error Budget

For a 99.9% monthly availability target:

| Period | Allowed Downtime |
|---|---:|
| Daily | ~1.44 minutes |
| Weekly | ~10.1 minutes |
| Monthly | ~43.8 minutes |

The error budget should guide release decisions. If the platform consumes too much error budget, feature releases should pause while reliability improvements are prioritized.

## Latency Baseline

The local performance benchmark established the following baseline:

| Metric | Baseline |
|---|---:|
| Average `/predict` latency | ~76 ms |
| TensorFlow warm inference | ~59 ms |
| PyTorch warm inference | ~11 ms |
| Batch throughput | ~19 images/sec |

These values are local development baselines and should be remeasured in Cloud Run.

## Alert Thresholds

| Alert | Warning | Critical |
|---|---:|---:|
| API Error Rate | > 1% for 10 minutes | > 5% for 5 minutes |
| P95 Predict Latency | > 150 ms for 15 minutes | > 300 ms for 10 minutes |
| Health Check Failure | 2 consecutive failures | 5 consecutive failures |
| Cache Hit Rate | < 80% | < 50% |
| Memory Utilization | > 75% | > 90% |
| CPU Utilization | > 70% | > 90% |
| Deployment Failure | 1 failed deployment | repeated failed deployments |

## Operational Notes

- SLOs should be reviewed after every major architecture change.
- Cloud Run performance should be compared against local benchmark results.
- P95 and P99 latency are more important than average latency for production monitoring.
- Cold starts should be tracked separately from warm request latency.
- Model version changes should trigger benchmark comparisons.

## Future Improvements

- Add Prometheus-compatible metrics.
- Integrate Google Cloud Monitoring dashboards.
- Publish benchmark reports as GitHub Actions artifacts.
- Add automated SLO checks in CI/CD.
- Add model-specific latency dashboards.
- Track latency by framework, category, and model version.
