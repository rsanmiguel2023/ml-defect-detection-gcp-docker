"""
REST API routes.
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.inference import predict_image
from app.schemas import PredictionResponse

router = APIRouter()


@router.get("/version")
def version():
    return {
        "tensorflow": "available",
        "pytorch": "available",
        "mlflow": "enabled",
    }


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    framework: str = Form("tensorflow"),
    category: str = Form("bottle"),
):
    try:
        image_bytes = await file.read()
        result = predict_image(
            image_bytes=image_bytes,
            framework=framework,
            category=category,
        )
        return PredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        ) from error
