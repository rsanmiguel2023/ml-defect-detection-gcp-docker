"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    framework: str
    category: str
    prediction: str
    confidence: float
