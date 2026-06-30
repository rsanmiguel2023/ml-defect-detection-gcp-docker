# Stage 2: Google Cloud Storage Setup

This stage connects the project to Google Cloud Storage (GCS) without storing the dataset in GitHub.

## Goal

- Create a GCP project or use an existing one
- Create a Cloud Storage bucket
- Upload the MVTec AD dataset to the bucket
- Validate that Python can connect to the bucket
- Keep credentials and raw data out of GitHub

## Recommended GCS layout

```text
gs://YOUR_BUCKET_NAME/
  raw/
    mvtec/
  processed/
  models/
    tensorflow/
    pytorch/
  reports/
```

## Local `.env` example

Create a local `.env` file from `.env.example` and update the values.

```text
GCP_PROJECT_ID=your-gcp-project-id
GCP_BUCKET_NAME=your-unique-bucket-name
GCP_RAW_PREFIX=raw/mvtec
GCP_PROCESSED_PREFIX=processed
GCP_MODEL_PREFIX=models
LOCAL_DATA_DIR=data/raw/mvtec
GOOGLE_APPLICATION_CREDENTIALS=secrets/gcp-service-account.json
```

Never commit `.env` or service account JSON files.

## Commands

Create bucket:

```bash
gcloud storage buckets create gs://YOUR_BUCKET_NAME --location=us-central1
```

Upload dataset:

```bash
gcloud storage cp -r data/raw/mvtec gs://YOUR_BUCKET_NAME/raw/
```

List uploaded files:

```bash
gcloud storage objects list gs://YOUR_BUCKET_NAME/raw/mvtec/**
```

Validate Python connection:

```bash
python scripts/validate_gcs_connection.py
```

## Definition of done

- GCS bucket exists
- Dataset is uploaded to `raw/mvtec`
- `.env` is configured locally
- Python connection test succeeds
- No dataset files or secrets are committed
