"""
Entry point for the PyTorch training pipeline.
"""

import argparse

from pytorch_pipeline.evaluate import evaluate_pytorch_model
from pytorch_pipeline.train import train_pytorch_model


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["train", "evaluate"],
        required=True,
    )

    parser.add_argument(
        "--category",
        default="bottle",
    )

    args = parser.parse_args()

    if args.mode == "train":
        train_pytorch_model(category=args.category)
    else:
        evaluate_pytorch_model(category=args.category)


if __name__ == "__main__":
    main()
