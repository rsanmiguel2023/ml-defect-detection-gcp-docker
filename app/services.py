"""
Application service layer.
"""

from app.schemas import EvaluationResponse
from src.pytorch_pipeline.evaluate import evaluate_pytorch_model
from src.tensorflow_pipeline.evaluate import evaluate_tensorflow_model


def run_model_evaluation(framework: str, category: str) -> EvaluationResponse:
    framework = framework.lower()

    if framework == "tensorflow":
        evaluate_tensorflow_model(category=category)
        return EvaluationResponse(
            framework=framework,
            category=category,
            status="completed",
            report_file="reports/tensorflow_classification_report.csv",
            confusion_matrix_file="reports/tensorflow_confusion_matrix.csv",
        )

    if framework == "pytorch":
        evaluate_pytorch_model(category=category)
        return EvaluationResponse(
            framework=framework,
            category=category,
            status="completed",
            report_file="reports/pytorch_classification_report.csv",
            confusion_matrix_file="reports/pytorch_confusion_matrix.csv",
        )

    raise ValueError("framework must be either 'tensorflow' or 'pytorch'")
