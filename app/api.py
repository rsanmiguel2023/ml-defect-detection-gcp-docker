"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from app.observability import RequestContextMiddleware
from app.routes import router
from app.security import SecurityHeadersMiddleware

app = FastAPI(
    title="Industrial Defect Detection API",
    version="1.0.0",
    description="TensorFlow and PyTorch industrial defect detection service.",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestContextMiddleware)

app.include_router(router)


@app.get("/")
def root():
    return {
        "application": "Industrial Defect Detection",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
