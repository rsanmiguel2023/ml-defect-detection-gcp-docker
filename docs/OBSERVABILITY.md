# Observability

## Overview

This project implements a production-oriented observability layer for the Industrial Defect Detection platform. The observability components provide operational visibility into API requests, model inference, application health, and model cache utilization.

The objective is to make the application easier to monitor, troubleshoot, and operate in cloud-native environments such as Google Cloud Run and future Kubernetes deployments.

---

# Features

The platform currently supports the following observability capabilities:

- Structured JSON request logging
- Structured prediction logging
- Request tracing using unique Request IDs
- Health endpoint
- Readiness endpoint
- Metrics endpoint
- Model cache statistics
- Prediction latency tracking
- Model version tracking
- Image size tracking

---

# Architecture

```
                Client
                   │
                   │ HTTP Request
                   ▼
        FastAPI Request Middleware
                   │
        Generates Request ID
                   │
        Measures Request Latency
                   │
         Logs Request Metadata
                   ▼
            Prediction Service
                   │
         Loads Cached Model
                   │
        Performs Inference
                   │
      Logs Prediction Metadata
                   ▼
               Response
```

---

# Request Lifecycle

Each request passes through the following stages:

1. Request received
2. Request ID generated (or reused if provided)
3. Request timer started
4. Model inference executed
5. Prediction logged
6. Response latency calculated
7. Structured request log written
8. Response returned to client

---

# Request IDs

Every API request receives a unique Request ID.

Example response header:

```
X-Request-ID: 48ef32ab-f98c-4d1b-a8f4-bd72ef7b08fd
```

Request IDs allow production issues to be traced through application logs and cloud logging platforms.

---

# Structured Request Logging

Instead of plain text logs, the application writes structured JSON logs.

Example:

```json
{
  "event": "request_completed",
  "request_id": "48ef32ab-f98c-4d1b-a8f4-bd72ef7b08fd",
  "method": "POST",
  "path": "/predict",
  "status_code": 200,
  "latency_ms": 41.27
}
```

Benefits include:

- Machine-readable logs
- Easier filtering
- Cloud Logging compatibility
- Log aggregation support
- Future SIEM integration

---

# Prediction Logging

Each prediction generates a structured inference log.

Example:

```json
{
  "event": "prediction_completed",
  "framework": "tensorflow",
  "category": "bottle",
  "model_version": "v1",
  "prediction": "good",
  "confidence": 0.9984,
  "latency_ms": 38.72,
  "image_size_bytes": 1048576
}
```

Captured metadata includes:

| Field | Description |
|---------|-------------|
| Framework | TensorFlow or PyTorch |
| Category | MVTec AD category |
| Model Version | Version used for inference |
| Prediction | Predicted class |
| Confidence | Prediction confidence |
| Latency | Inference execution time |
| Image Size | Uploaded image size |

---

# Model Cache Monitoring

The application caches loaded models to minimize repeated disk access and improve inference performance.

Current cache statistics include:

- Number of cached models
- Cache hits
- Cache misses
- Loaded model identifiers

Example:

```json
{
  "cached_models": 3,
  "cache_hits": 127,
  "cache_misses": 5,
  "cache_keys": [
    "tensorflow:bottle:v1",
    "tensorflow:cable:v1",
    "pytorch:bottle:v1"
  ]
}
```

---

# Health Endpoint

```
GET /health
```

Purpose:

Determines whether the application process is running.

Example response:

```json
{
  "status": "healthy"
}
```

---

# Readiness Endpoint

```
GET /ready
```

Purpose:

Indicates whether the application is ready to serve requests.

Example response:

```json
{
  "status": "ready"
}
```

This endpoint is intended for container orchestration platforms such as:

- Google Cloud Run
- Kubernetes
- Docker Swarm

---

# Metrics Endpoint

```
GET /metrics
```

Returns current runtime metrics.

Example:

```json
{
  "cached_models": 3,
  "cache_hits": 127,
  "cache_misses": 5
}
```

Future versions will expose Prometheus-compatible metrics.

---

# Cache Endpoint

```
GET /cache
```

Returns detailed information regarding the model cache.

Example:

```json
{
  "cached_models": 3,
  "cache_hits": 127,
  "cache_misses": 5,
  "cache_keys": [
    "tensorflow:bottle:v1",
    "tensorflow:cable:v1",
    "pytorch:bottle:v1"
  ]
}
```

---

# Cloud Run Integration

The observability layer has been designed for deployment on Google Cloud Run.

The following Cloud Run capabilities are supported:

- Request logging
- Structured JSON logs
- Health monitoring
- Readiness monitoring
- Container lifecycle monitoring
- Request tracing

---

# Future Enhancements

The observability roadmap includes:

- Prometheus metrics export
- Grafana dashboards
- OpenTelemetry tracing
- Distributed tracing
- Cloud Monitoring dashboards
- Alerting policies
- Error rate monitoring
- Throughput metrics
- Model drift monitoring
- Data quality monitoring

---

# Operational Benefits

The observability layer enables operators to:

- Monitor API performance
- Diagnose production failures
- Track model utilization
- Measure inference latency
- Validate deployment health
- Monitor cache efficiency
- Troubleshoot client requests using Request IDs

These capabilities improve system reliability and provide a foundation for enterprise-grade monitoring and operations.