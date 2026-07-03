"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    framework: str
    category: str
    prediction: str
    confidence: float


class BatchPredictionItem(BaseModel):
    filename: str
    prediction: str
    confidence: float


class BatchPredictionResponse(BaseModel):
    framework: str
    category: str
    results: list[BatchPredictionItem]
