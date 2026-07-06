# Operations Runbook

## Overview

This runbook provides operational procedures for supporting the Industrial Defect Detection platform.

It covers common failure scenarios, investigation steps, mitigation actions, and validation checks.

## Quick Health Checks

Run these checks first during any incident:

```bash
curl https://<cloud-run-url>/health
curl https://<cloud-run-url>/ready
curl https://<cloud-run-url>/metrics
curl https://<cloud-run-url>/cache
```

Expected:

- `/health` returns healthy.
- `/ready` returns ready.
- `/metrics` returns cache and runtime metrics.
- `/cache` returns model cache statistics.

## Scenario 1: API Is Unavailable

### Symptoms

- `/health` fails.
- Cloud Run returns 5xx.
- Users cannot access predictions.

### Investigation

1. Check Cloud Run service status.
2. Review latest deployment.
3. Inspect Cloud Run logs.
4. Confirm container image exists in Artifact Registry.
5. Validate service account permissions.
6. Check environment variables.

### Mitigation

- Roll back to the previous Cloud Run revision.
- Redeploy the last known good image.
- Restore missing environment variables.
- Increase CPU or memory if the service is crashing.

### Validation

```bash
curl https://<cloud-run-url>/health
```

Confirm 200 response.

## Scenario 2: Model Fails to Load

### Symptoms

- Prediction endpoint returns 500.
- Logs show model path or version error.
- `/cache` does not show expected model.

### Investigation

1. Check requested framework, category, and model version.
2. Verify model exists under the expected path.
3. Confirm the model registry can resolve `latest`.
4. Review Artifact Registry and Cloud Storage dependencies.
5. Confirm service account access.

### Mitigation

- Restore missing model files.
- Revert to a known good model version.
- Update model registry configuration.
- Redeploy the API if required.

## Scenario 3: High Prediction Latency

### Symptoms

- P95 `/predict` latency exceeds target.
- Users report slow predictions.
- Cloud Run CPU or memory utilization is high.

### Investigation

1. Compare latency against benchmark baseline.
2. Check cache hit rate.
3. Look for cold starts.
4. Review model load frequency.
5. Check request volume and batch sizes.
6. Review CPU and memory metrics.

### Mitigation

- Increase Cloud Run CPU or memory.
- Enable minimum instances.
- Reduce model reloads.
- Optimize preprocessing.
- Use batch prediction when appropriate.

## Scenario 4: Deployment Failure

### Symptoms

- GitHub Actions deploy job fails.
- New Cloud Run revision is not created.
- Image push or deploy command fails.

### Investigation

1. Review GitHub Actions logs.
2. Confirm Workload Identity Federation configuration.
3. Validate Artifact Registry permissions.
4. Confirm Cloud Run deploy permissions.
5. Check image path and tag.

### Mitigation

- Fix CI/CD secret or WIF configuration.
- Restore IAM permissions.
- Re-run workflow.
- Manually deploy last known good image if needed.

## Scenario 5: Cache Hit Rate Drops

### Symptoms

- `/cache` shows low hit rate.
- Prediction latency increases.
- Repeated model loading appears in logs.

### Investigation

1. Check model version parameter usage.
2. Confirm whether requests use `latest` or explicit versions.
3. Review model registry cache behavior.
4. Check if the service is frequently restarting.

### Mitigation

- Use stable explicit model versions for production.
- Reduce unnecessary model version churn.
- Investigate container restarts.
- Enable minimum instances.

## Rollback Procedure

1. Identify last known good Cloud Run revision.
2. Route traffic back to the previous revision.
3. Confirm `/health` and `/ready`.
4. Run a test prediction.
5. Monitor error rate and latency for at least 15 minutes.

## Post-Recovery Checklist

- Confirm service health.
- Confirm prediction endpoint.
- Confirm batch endpoint.
- Check error rate.
- Check P95 latency.
- Confirm cache hit rate.
- Document timeline and root cause.
