# Production Operations Guide

## Overview

This guide describes the operational model for running and maintaining the Industrial Defect Detection platform.

It covers deployment, verification, monitoring, backup, recovery, version management, and maintenance practices.

## Operating Model

The platform is operated as a cloud-native MLOps service with:

- FastAPI inference API
- TensorFlow and PyTorch model support
- Versioned model registry
- Dockerized runtime
- Cloud Run deployment
- GitHub Actions CI/CD
- Terraform-managed infrastructure
- Structured logging
- Benchmark reporting
- Security and testing controls

## Deployment Workflow

1. Developer creates feature branch from `dev`.
2. Changes are committed and pushed.
3. Pull request is opened against `dev`.
4. CI runs linting, formatting, tests, security scan, and build validation.
5. PR is reviewed and merged into `dev`.
6. Deployment workflow builds container image.
7. Image is pushed to Artifact Registry.
8. Cloud Run service is updated.
9. Health checks validate deployment.

## Post-Deployment Verification

After deployment, validate:

```bash
curl https://<cloud-run-url>/health
curl https://<cloud-run-url>/ready
curl https://<cloud-run-url>/models
curl https://<cloud-run-url>/metrics
curl https://<cloud-run-url>/cache
```

Also verify:

- Swagger docs load successfully.
- Single prediction works.
- Batch prediction works.
- Logs contain request IDs.
- Cache statistics update after predictions.

## Model Version Management

Production model serving should use explicit model versions when possible.

Recommended practices:

- Use `latest` only in development or controlled testing.
- Use explicit versions such as `v1`, `v2`, or `v3` in production.
- Benchmark every new model version.
- Keep previous versions available for rollback.
- Track predictions by framework, category, and model version.

## Backup and Recovery

Recommended backup targets:

- Source code repository
- Terraform configuration
- Cloud Run deployment configuration
- Model artifacts
- Benchmark reports
- Operational documentation

Recovery should prioritize:

1. Restore API availability.
2. Restore model loading.
3. Validate prediction behavior.
4. Confirm latency and error rate.
5. Monitor for recurrence.

## Capacity Planning

Review the following regularly:

- Request volume
- P95 and P99 latency
- Batch throughput
- Cloud Run CPU utilization
- Cloud Run memory utilization
- Cold starts
- Model cache hit rate
- Deployment frequency

Use benchmark results as the baseline for capacity planning.

## Maintenance Schedule

| Activity | Frequency |
|---|---|
| Dependency vulnerability review | Monthly |
| Terraform plan review | Monthly |
| Benchmark refresh | Per major release |
| SLO review | Quarterly |
| Runbook review | Quarterly |
| Model version cleanup | As needed |
| CI/CD workflow review | Quarterly |

## Production Readiness Checklist

- CI checks passing.
- Tests passing.
- Terraform validated.
- Docker image builds.
- Cloud Run deploys successfully.
- Health and readiness endpoints pass.
- Security headers enabled.
- Request logging enabled.
- Model registry operational.
- Benchmark report updated.
- Runbook and alert documentation available.

## Future Operations Enhancements

- Cloud Monitoring dashboards.
- SLO burn-rate alerts.
- Prometheus metrics.
- Grafana dashboard.
- Synthetic monitoring.
- Load testing.
- Automated rollback.
- Dependency lock-file strategy.
