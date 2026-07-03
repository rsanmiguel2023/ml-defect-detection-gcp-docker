"""
REST API routes.
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import SUPPORTED_CATEGORIES, SUPPORTED_FRAMEWORKS
from app.inference import predict_batch_images, predict_image
from app.model_registry import registry
from app.schemas import BatchPredictionResponse, EvaluationResponse, PredictionResponse
from app.services import run_model_evaluation

router = APIRouter()


@router.get("/version")
def version():
    return {
        "tensorflow": "available",
        "pytorch": "available",
        "mlflow": "enabled",
    }


@router.get("/models")
def list_models():
    models = {}

    for framework in SUPPORTED_FRAMEWORKS:
        models[framework] = {}

        for category in SUPPORTED_CATEGORIES:
            versions = registry.list_versions(framework, category)

            if versions:
                models[framework][category] = versions

    return models


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    framework: str = Form("tensorflow"),
    category: str = Form("bottle"),
    model_version: str = Form("latest"),
):
    try:
        image_bytes = await file.read()

        result = predict_image(
            image_bytes=image_bytes,
            framework=framework,
            category=category,
            model_version=model_version,
        )

        return PredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        ) from error


@router.post("/predict-batch", response_model=BatchPredictionResponse)
async def predict_batch(
    files: list[UploadFile] = File(...),
    framework: str = Form("tensorflow"),
    category: str = Form("bottle"),
    model_version: str = Form("latest"),
):
    try:
        image_files = []

        for file in files:
            image_bytes = await file.read()
            image_files.append((file.filename, image_bytes))

        result = predict_batch_images(
            files=image_files,
            framework=framework,
            category=category,
            model_version=model_version,
        )

        return BatchPredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(error)}",
        ) from error


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(
    framework: str = Form("tensorflow"),
    category: str = Form("bottle"),
):
    try:
        return run_model_evaluation(
            framework=framework,
            category=category,
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(error)}",
        ) from error


@router.get("/ready")
def ready():
    return {
        "status": "ready",
    }


@router.get("/cache")
def cache():
    return registry.cache_stats()


@router.get("/metrics")
def metrics():
    stats = registry.cache_stats()

    return {
        "cached_models": stats["cached_models"],
        "cache_hits": stats["cache_hits"],
        "cache_misses": stats["cache_misses"],
    }
