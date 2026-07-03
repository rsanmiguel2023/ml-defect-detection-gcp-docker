"""
Command runner for PyTorch pipeline.
"""

import argparse

from src.pytorch_pipeline.evaluate import evaluate_pytorch_model
from src.pytorch_pipeline.train import train_pytorch_model


def main():
    parser = argparse.ArgumentParser(description="Run PyTorch ML pipeline")

    parser.add_argument(
        "--mode",
        choices=["train", "evaluate"],
        required=True,
        help="Choose whether to train or evaluate the PyTorch model",
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
        train_pytorch_model(
            category=args.category,
            model_version=args.model_version,
        )

    if args.mode == "evaluate":
        evaluate_pytorch_model(category=args.category)


if __name__ == "__main__":
    main()
