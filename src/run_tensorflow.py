"""
Command runner for TensorFlow pipeline.
"""

import argparse

from src.tensorflow_pipeline.evaluate import evaluate_tensorflow_model
from src.tensorflow_pipeline.train import train_tensorflow_model


def main():
    parser = argparse.ArgumentParser(description="Run TensorFlow ML pipeline")

    parser.add_argument(
        "--mode",
        choices=["train", "evaluate"],
        required=True,
        help="Choose whether to train or evaluate the TensorFlow model",
    )

    parser.add_argument(
        "--category",
        default="bottle",
        help="MVTec AD category to train or evaluate",
    )

    parser.add_argument(
        "--model-version",
        default="v1",
        help="Model version to train or evaluate",
    )

    args = parser.parse_args()

    if args.mode == "train":
        train_tensorflow_model(
            category=args.category,
            model_version=args.model_version,
        )

    if args.mode == "evaluate":
        evaluate_tensorflow_model(category=args.category)


if __name__ == "__main__":
    main()
