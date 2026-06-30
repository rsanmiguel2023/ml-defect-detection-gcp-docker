# Project Build Stages

## Stage 1: GitHub scaffold
- Repository structure
- Dockerfile and docker-compose
- GCP configuration
- Streamlit shell
- Placeholder training files

## Stage 2: GCP dataset workflow and TensorFlow model
- Upload MVTec AD to Cloud Storage
- Download selected category locally
- Train TensorFlow EfficientNetB0
- Save model artifact

## Stage 3: PyTorch model
- Train PyTorch ResNet18 on same classification task
- Save model artifact

## Stage 4: Evaluation
- Compare accuracy, precision, recall, F1-score, inference time, and model size

## Stage 5: Streamlit inference app
- Upload image
- Run TensorFlow and PyTorch predictions
- Display model confidence

## Stage 6: Cloud Run deployment
- Build production Docker image
- Push to Artifact Registry
- Deploy to Cloud Run
