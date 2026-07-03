"""
Inference utilities for TensorFlow and PyTorch models.
"""

from io import BytesIO

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from app.model_registry import registry

CLASS_NAMES = ["defective", "good"]


def load_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image


def predict_tensorflow(image: Image.Image, category: str):
    model = registry.load_tensorflow(category)

    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))

    return CLASS_NAMES[predicted_index], confidence


def predict_pytorch(image: Image.Image, category: str):
    model = registry.load_pytorch(category)

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


def predict_image(image_bytes: bytes, framework: str, category: str):
    image = load_image(image_bytes)

    framework = framework.lower()

    if framework == "tensorflow":
        prediction, confidence = predict_tensorflow(image, category)
    elif framework == "pytorch":
        prediction, confidence = predict_pytorch(image, category)
    else:
        raise ValueError("framework must be either 'tensorflow' or 'pytorch'")

    return {
        "framework": framework,
        "category": category,
        "prediction": prediction,
        "confidence": confidence,
    }


def predict_batch_images(files: list, framework: str, category: str):
    results = []

    for filename, image_bytes in files:
        prediction = predict_image(
            image_bytes=image_bytes,
            framework=framework,
            category=category,
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
        "results": results,
    }
