"""
Command runner for TensorFlow pipeline.
"""

import argparse

from src.tensorflow_pipeline.evaluate import evaluate_tensorflow_model
from src.tensorflow_pipeline.train import train_tensorflow_model


def main():
    parser = argparse.ArgumentParser(description="Run TensorFlow ML pipeline")

    parser.add_argument("--mode", choices=["train", "evaluate"], required=True)
    parser.add_argument("--category", default="bottle")
    parser.add_argument("--model-version", default="v1")

    args = parser.parse_args()

    if args.mode == "train":
        train_tensorflow_model(
            category=args.category,
            model_version=args.model_version,
        )

    if args.mode == "evaluate":
        evaluate_tensorflow_model(
            category=args.category,
            model_version=args.model_version,
        )


if __name__ == "__main__":
    main()
