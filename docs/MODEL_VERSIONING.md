# Model Versioning

This project supports versioned TensorFlow and PyTorch models for each MVTec AD category.

## Model Directory Structure

```text
models/
├── tensorflow/
│   └── bottle/
│       └── v1/
│           └── model.keras
│
└── pytorch/
    └── bottle/
        └── v1/
            └── model.pt
```

## Supported Version Selection

The API supports selecting a specific model version:

```text
v1
v2
v3
```

It also supports:

```text
latest
```

`latest` resolves to the most recent available version for the selected framework and category.

## API Endpoints

### List available models

```http
GET /models
```

### Single prediction

```http
POST /predict
```

Required form fields:

```text
file
framework
category
model_version
```

### Batch prediction

```http
POST /predict-batch
```

Required form fields:

```text
files
framework
category
model_version
```

## Example

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample.png" \
  -F "framework=tensorflow" \
  -F "category=bottle" \
  -F "model_version=latest"
```