# Alerting Strategy

## Overview

This document defines the alerting strategy for the Industrial Defect Detection platform.

The alerting model focuses on reliability, latency, prediction failures, model availability, infrastructure health, and deployment safety.

## Alert Severity Levels

| Severity | Description | Response Target |
|---|---|---:|
| SEV-1 | Service unavailable or production prediction failure | Immediate |
| SEV-2 | Major degradation affecting predictions or deployments | < 30 minutes |
| SEV-3 | Partial degradation or elevated risk | < 4 hours |
| SEV-4 | Informational or maintenance item | Next business day |

## Core Alerts

| Alert | Severity | Trigger | Impact | Initial Response |
|---|---|---|---|---|
| API Unavailable | SEV-1 | `/health` fails repeatedly | Service cannot accept requests | Check Cloud Run status and recent deployment |
| High Error Rate | SEV-2 | 5xx rate > 5% for 5 minutes | Users experience failed predictions | Review application logs and recent changes |
| Elevated Prediction Latency | SEV-2 | P95 `/predict` latency > 300 ms | User experience degradation | Check CPU, memory, cache, and model load logs |
| Warning Prediction Latency | SEV-3 | P95 `/predict` latency > 150 ms for 15 minutes | Risk of SLO breach | Review traffic and warm/cold request split |
| Model Load Failure | SEV-1 | Model registry fails to load selected model | Prediction unavailable | Validate model path, version, and artifact availability |
| Cache Hit Rate Drop | SEV-3 | Cache hit rate < 80% | Increased latency and disk access | Review model version churn and cache behavior |
| Cloud Run Memory Pressure | SEV-2 | Memory utilization > 90% | Possible container restarts | Increase memory allocation or optimize model loading |
| Cloud Run CPU Saturation | SEV-3 | CPU utilization > 90% sustained | Latency degradation | Increase CPU allocation or scale configuration |
| Deployment Failure | SEV-2 | GitHub Actions deployment fails | Release blocked | Review CI logs and Cloud Run deploy logs |
| Artifact Registry Access Failure | SEV-2 | Image pull fails | Deployment or startup failure | Validate IAM and image path |
| Storage Access Failure | SEV-2 | Cloud Storage access denied or unavailable | Model or data retrieval risk | Validate IAM, bucket status, and object paths |

## Alert Response Workflow

1. Confirm alert validity.
2. Check recent deployments and configuration changes.
3. Review Cloud Run logs.
4. Check `/health`, `/ready`, `/metrics`, and `/cache`.
5. Confirm model version and framework.
6. Identify whether the issue is application, model, infrastructure, or dependency related.
7. Mitigate by rollback, scaling, disabling a bad model version, or restoring service.
8. Document timeline and root cause.

## Recommended Monitoring Signals

- Request count
- Request latency
- Error rate
- Prediction count
- Prediction latency by framework
- Prediction latency by category
- Prediction latency by model version
- Cache hits and misses
- Model load duration
- Cold starts
- Cloud Run CPU utilization
- Cloud Run memory utilization
- Container restart count
- Deployment success rate

## Future Enhancements

- Cloud Monitoring alert policies.
- Prometheus metrics export.
- Slack or email notification routing.
- SLO-based alerting.
- Error budget burn-rate alerts.
- Model drift and data-quality alerts.
