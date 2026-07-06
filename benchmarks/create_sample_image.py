"""
Create a small synthetic image for API benchmarking.
"""

from pathlib import Path

from PIL import Image


def create_sample_image(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (224, 224), color=(240, 240, 240))
    image.save(output_path)
    return output_path


if __name__ == "__main__":
    create_sample_image(Path("results") / "benchmarks" / "sample.png")
