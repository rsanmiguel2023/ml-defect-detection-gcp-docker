# Cloud-Based Industrial Defect Detection

This project is a staged machine learning and MLOps portfolio project for industrial defect detection using:

- TensorFlow
- PyTorch
- Docker
- Google Cloud Storage
- Streamlit
- GitHub

The goal is to build the project realistically in stages, without overclaiming completed work before it is actually implemented.

## Current Status

**Stage 1 complete:** repository scaffold, Docker setup, GCP configuration, and Streamlit shell.

Model training and deployment will be added in later stages.

## Planned Dataset

The project will use the MVTec AD industrial anomaly detection dataset.

The dataset will not be committed to GitHub. It will be stored in Google Cloud Storage.

Planned GCS layout:

```text
gs://your-bucket-name/
├── raw/mvtec/
├── processed/
├── models/
└── predictions/
```

## Planned Models

| Framework | Model | Status |
|---|---|---|
| TensorFlow | EfficientNetB0 | Planned for Stage 2 |
| PyTorch | ResNet18 | Planned for Stage 3 |

## Repository Structure

```text
ml-defect-detection-gcp-docker/
├── app/
│   └── streamlit_app.py
├── data/
│   └── README.md
├── docs/
│   └── STAGES.md
├── models/
│   └── README.md
├── notebooks/
├── reports/
│   ├── figures/
│   └── metrics.md
├── src/
│   ├── config.py
│   ├── evaluate.py
│   ├── gcp_storage.py
│   ├── predict.py
│   ├── preprocess.py
│   ├── train_pytorch.py
│   └── train_tensorflow.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Local Setup

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` with your own GCP project and bucket name.

## Run with Docker

Build the image:

```bash
docker build -t defect-detector .
```

Run the Streamlit app:

```bash
docker compose up
```

Open:

```text
http://localhost:8501
```

## Project Stages

See [`docs/STAGES.md`](docs/STAGES.md).

## Important Notes

- Dataset files are excluded from GitHub.
- Trained models are excluded from GitHub.
- GCP will store dataset and model artifacts.
- GitHub will store source code, documentation, and reproducible setup instructions.

## Stage 2: GCP Storage

The project uses Google Cloud Storage for raw image data and future model artifacts. See:

```text
docs/GCP_STORAGE_SETUP.md
```

This keeps large dataset files and credentials out of GitHub.


## TensorFlow Training Pipeline

This stage trains an EfficientNetB0 image classification model using TensorFlow.

## Run training locally

```bash
python src/run_tensorflow.py --mode train
```
## Run evaluation locally

```bash
python src/run_tensorflow.py --mode evaluate
```


## MLflow Experiment Tracking

This project uses MLflow to track TensorFlow and PyTorch model experiments.

### Start MLflow UI

```bash
mlflow ui
```