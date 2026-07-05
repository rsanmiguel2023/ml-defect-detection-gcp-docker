# Terraform Infrastructure

## Overview

This directory contains Terraform configuration for provisioning the Google Cloud infrastructure used by the Industrial Defect Detection platform.

## Managed Resources

Terraform provisions:

- Required Google Cloud APIs
- Artifact Registry Docker repository
- Cloud Storage bucket
- Cloud Run runtime service account
- IAM permissions
- Cloud Run service
- Terraform outputs

## Prerequisites

- Terraform installed
- Google Cloud CLI installed
- Authenticated with Google Cloud

```bash
gcloud auth login
gcloud auth application-default login
```

## Configuration

Create a local `terraform.tfvars` file:

```hcl
project_id = "ml-defect-detection-rob"
region     = "us-central1"

artifact_registry_repository = "ml-defect-detection"
cloud_run_service_name       = "ml-defect-api"
storage_bucket_name          = "ml-defect-detection-rsanmiguel2023"

environment = "dev"
```

Do not commit `terraform.tfvars`.

## Usage

Initialize Terraform:

```bash
terraform init
```

Format files:

```bash
terraform fmt
```

Validate configuration:

```bash
terraform validate
```

Preview infrastructure changes:

```bash
terraform plan
```

Apply infrastructure changes:

```bash
terraform apply
```

## Outputs

Terraform outputs:

- Project ID
- Region
- Artifact Registry repository
- Storage bucket name
- Storage bucket URL
- Cloud Run service account email
- Cloud Run service URL

## Notes

This Terraform configuration is designed for the current development environment. Future improvements may introduce reusable modules and separate environment folders for dev, test, and production.