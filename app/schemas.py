"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    framework: str
    category: str
    model_version: str
    prediction: str
    confidence: float


class BatchPredictionItem(BaseModel):
    filename: str
    prediction: str
    confidence: float


class BatchPredictionResponse(BaseModel):
    framework: str
    category: str
    model_version: str
    results: list[BatchPredictionItem]


class EvaluationResponse(BaseModel):
    framework: str
    category: str
    status: str
    report_file: str
    confusion_matrix_file: str
