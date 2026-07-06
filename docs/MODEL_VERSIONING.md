# Model Versioning

## Versioning Strategy

Models are versioned independently for each framework and category.

Supported versions:

- v1
- v2
- v3
- latest

`latest` resolves to the newest validated production model.

Older versions remain available until validation confirms they can be retired.

## Directory Structure

```text
models/
├── tensorflow/
└── pytorch/
```

## API Support

- GET /models
- POST /predict
- POST /predict-batch
