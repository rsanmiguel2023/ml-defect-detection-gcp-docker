# Cloud-Based Industrial Defect Detection

> An end-to-end Machine Learning and MLOps project demonstrating industrial image defect detection using TensorFlow, PyTorch, FastAPI, Docker, Terraform, GitHub Actions, and Google Cloud Platform.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-2.3-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-success)

---

# Project Overview

This project demonstrates a complete production-oriented Machine Learning workflow for industrial visual defect detection using the MVTec AD dataset.

The repository was built incrementally using a staged engineering approach, progressing from data ingestion through model training, API development, cloud deployment, infrastructure automation, testing, observability, benchmarking, and production operations.

The goal is not only to train image classification models, but also to demonstrate the engineering practices required to deploy and operate machine learning workloads in a cloud-native environment.

---

# Key Features

- TensorFlow EfficientNetB0 training pipeline
- PyTorch ResNet18 training pipeline
- Versioned model registry
- FastAPI REST API
- Batch prediction endpoint
- Streamlit demonstration application
- Docker containerization
- Google Cloud Storage integration
- Artifact Registry
- Cloud Run deployment
- Terraform Infrastructure as Code
- GitHub Actions CI/CD
- Security hardening
- Structured logging
- Health and readiness endpoints
- Model cache
- Performance benchmarking
- Production operations documentation

---

# Solution Architecture

```text
                  Client
                     │
                     ▼
               FastAPI REST API
                     │
        ┌────────────┴────────────┐
        │                         │
 TensorFlow               PyTorch
 EfficientNetB0           ResNet18
        │                         │
        └────────────┬────────────┘
                     │
             Versioned Model Registry
                     │
             Google Cloud Storage
                     │
              Cloud Run Deployment
                     │
          Terraform Infrastructure
```

---

# Technology Stack

## Machine Learning

- TensorFlow
- PyTorch
- scikit-learn
- OpenCV
- Pillow

## Backend

- FastAPI
- Uvicorn
- Pydantic

## Cloud

- Google Cloud Storage
- Artifact Registry
- Cloud Run

## Infrastructure

- Terraform
- Docker
- Docker Compose

## CI/CD

- GitHub Actions
- Ruff
- Black
- isort
- pytest
- pip-audit

---

# Repository Structure

```text
app/
benchmarks/
docs/
models/
notebooks/
reports/
results/
scripts/
src/
terraform/
tests/

Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

# Local Development

Clone the repository

```bash
git clone <repository-url>
cd ml-defect-detection-gcp-docker
```

Create a virtual environment

```bash
python -m venv .venv
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create your environment file

```bash
cp .env.example .env
```

Run the API

```bash
uvicorn app.main:app --reload
```

Swagger UI

```text
http://localhost:8000/docs
```

---

# Docker

Build

```bash
docker build -t ml-defect-api .
```

Run

```bash
docker compose up
```

---

# Infrastructure

Infrastructure is provisioned using Terraform.

Resources include:

- Google Cloud Storage
- Artifact Registry
- Cloud Run
- Required Google APIs
- IAM configuration

Terraform files are located in

```text
terraform/
```

---

# CI/CD

GitHub Actions automatically performs:

- Ruff
- Black
- isort
- pytest
- pip-audit
- Docker build validation
- Terraform validation

---

# Security

Security controls include:

- Workload Identity Federation
- Least-privilege IAM
- FastAPI security headers
- Dependency vulnerability scanning
- Public Access Prevention
- Uniform Bucket-Level Access

See:

```text
docs/SECURITY.md
```

---

# Observability

Operational observability includes:

- Structured JSON logging
- Request IDs
- Health endpoint
- Readiness endpoint
- Metrics endpoint
- Cache statistics
- Prediction logging

See:

```text
docs/OBSERVABILITY.md
```

---

# Performance Benchmarking

The project includes automated benchmark tooling for:

- API latency
- Batch throughput
- TensorFlow inference
- PyTorch inference

Outputs include:

- CSV reports
- PNG charts
- SVG charts
- Markdown benchmark reports

See:

```text
docs/PERFORMANCE.md
```

---

# Production Operations

Operational documentation includes:

- Service Level Objectives
- Alerting strategy
- Incident response
- Operations dashboard
- Runbook
- Production operations guide

See:

```text
docs/SLOS.md
docs/ALERTING.md
docs/RUNBOOK.md
docs/OPERATIONS.md
```

---

# Documentation

| Document | Description |
|----------|-------------|
| STAGES.md | Project roadmap |
| SECURITY.md | Security controls |
| OBSERVABILITY.md | Monitoring strategy |
| MODEL_VERSIONING.md | Version management |
| CLOUD_RUN_DEPLOYMENT.md | Deployment guide |
| PERFORMANCE.md | Benchmark report |
| RUNBOOK.md | Operational procedures |
| INCIDENT_RESPONSE.md | Incident management |
| OPERATIONS.md | Production operations |

---

# Project Stages

The repository was developed incrementally across seventeen stages:

1. Project Scaffold
2. Google Cloud Storage
3. TensorFlow Training
4. PyTorch Training
5. Model Evaluation
6. Streamlit Application
7. FastAPI API
8. Docker
9. Artifact Registry
10. Cloud Run
11. Terraform
12. GitHub Actions
13. Security
14. Observability
15. Testing
16. Performance Benchmarking
17. Production Monitoring & Operations

---

# Future Enhancements

- Kubernetes deployment
- GPU inference
- Prometheus metrics
- Grafana dashboards
- OpenTelemetry
- Distributed tracing
- Model drift detection
- Data quality monitoring
- Automated canary deployments

---

# License

This project is intended for educational and portfolio purposes.