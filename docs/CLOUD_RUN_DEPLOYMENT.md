# Cloud Run Deployment

## Runtime Configuration

| Setting | Value |
|---|---|
| Region | us-central1 |
| Platform | Cloud Run |
| CPU | 2 |
| Memory | 4 GiB |
| Timeout | 300 seconds |
| Port | 8000 |
| Authentication | Public (unauthenticated) |

## Deployment

```bash
gcloud run deploy ml-defect-api \
  --image us-central1-docker.pkg.dev/.../ml-defect-api:latest
```

## Validation

- /health
- /ready
- /metrics
- /cache
- /models
