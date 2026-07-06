"""
Inference utilities for TensorFlow and PyTorch models.
"""

import time
from io import BytesIO

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from app.config import DEFAULT_MODEL_VERSION
from app.model_registry import registry
from app.observability import log_json

CLASS_NAMES = ["defective", "good"]


def load_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image


def predict_tensorflow(
    image: Image.Image,
    category: str,
    model_version: str = DEFAULT_MODEL_VERSION,
):
    model = registry.load_tensorflow(category, model_version)

    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))

    return CLASS_NAMES[predicted_index], confidence


def predict_pytorch(
    image: Image.Image,
    category: str,
    model_version: str = DEFAULT_MODEL_VERSION,
):
    model = registry.load_pytorch(category, model_version)

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_index = int(torch.argmax(probabilities, dim=1).item())
        confidence = float(probabilities[0][predicted_index].item())

    return CLASS_NAMES[predicted_index], confidence


def predict_image(
    image_bytes: bytes,
    framework: str,
    category: str,
    model_version: str = DEFAULT_MODEL_VERSION,
):
    start_time = time.perf_counter()

    image = load_image(image_bytes)

    framework = framework.lower()

    if framework == "tensorflow":
        prediction, confidence = predict_tensorflow(image, category, model_version)
    elif framework == "pytorch":
        prediction, confidence = predict_pytorch(image, category, model_version)
    else:
        raise ValueError("framework must be either 'tensorflow' or 'pytorch'")

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    log_json(
        "prediction_completed",
        framework=framework,
        category=category,
        model_version=model_version,
        prediction=prediction,
        confidence=confidence,
        latency_ms=latency_ms,
        image_size_bytes=len(image_bytes),
    )

    return {
        "framework": framework,
        "category": category,
        "model_version": model_version,
        "prediction": prediction,
        "confidence": confidence,
    }


def predict_batch_images(
    files: list,
    framework: str,
    category: str,
    model_version: str = DEFAULT_MODEL_VERSION,
):
    results = []

    for filename, image_bytes in files:
        prediction = predict_image(
            image_bytes=image_bytes,
            framework=framework,
            category=category,
            model_version=model_version,
        )

        results.append(
            {
                "filename": filename,
                "prediction": prediction["prediction"],
                "confidence": prediction["confidence"],
            }
        )

    return {
        "framework": framework,
        "category": category,
        "model_version": model_version,
        "results": results,
    }
