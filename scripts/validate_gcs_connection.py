"""Validate that the project can connect to Google Cloud Storage."""

from src.config import GCP_BUCKET_NAME, GCP_RAW_PREFIX
from src.gcp_storage import list_blobs


def main() -> None:
    if not GCP_BUCKET_NAME:
        raise SystemExit("GCP_BUCKET_NAME is missing. Create .env from .env.example first.")

    print(f"Checking bucket: gs://{GCP_BUCKET_NAME}")
    print(f"Checking prefix: {GCP_RAW_PREFIX}")

    objects = list_blobs(prefix=GCP_RAW_PREFIX, limit=10)

    if not objects:
        print("Connection succeeded, but no objects were found under the configured prefix.")
        print("Upload the dataset before starting model training.")
        return

    print("Connection succeeded. Sample objects:")
    for item in objects:
        print(f"- {item}")


if __name__ == "__main__":
    main()
