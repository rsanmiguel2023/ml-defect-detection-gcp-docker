"""
REST API routes.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
def version():
    return {
        "tensorflow": "available",
        "pytorch": "available",
        "mlflow": "enabled",
    }
