# Google Cloud Storage Setup

## Overview

This stage configures Cloud Storage for datasets, models, and reports.

## Recommended Layout

```text
raw/
processed/
models/
reports/
```

## Bucket Lifecycle

Recommended lifecycle policy:

- Retain raw datasets
- Archive older processed artifacts
- Keep production model versions
- Expire obsolete temporary files

## Validation

- Bucket created
- Dataset uploaded
- Python connection verified
- No secrets committed
