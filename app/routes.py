"""
REST API routes.
"""

from fastapi import APIRouter, File, Form, UploadFile

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
    return PredictionResponse(
        framework=framework,
        category=category,
        prediction="placeholder",
        confidence=0.0,
    )
