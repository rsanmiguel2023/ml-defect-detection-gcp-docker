from pathlib import Path


def summarize_dataset(data_dir: str) -> dict:
    """Return a lightweight count of image files by top-level folder."""
    root = Path(data_dir)
    image_exts = {".jpg", ".jpeg", ".png", ".bmp"}
    summary = {}

    if not root.exists():
        return summary

    for folder in sorted([p for p in root.iterdir() if p.is_dir()]):
        count = sum(1 for f in folder.rglob("*") if f.suffix.lower() in image_exts)
        summary[folder.name] = count

    return summary
