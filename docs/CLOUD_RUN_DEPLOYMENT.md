# Cloud Run Deployment

## Service URL

https://ml-defect-api-1054269542973.us-central1.run.app

## Artifact Registry Image

us-central1-docker.pkg.dev/ml-defect-detection-rob/ml-defect-detection/ml-defect-api:latest

## Deployment Command

```bash
gcloud run deploy ml-defect-api \
  --image us-central1-docker.pkg.dev/ml-defect-detection-rob/ml-defect-detection/ml-defect-api:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300