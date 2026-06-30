from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    gcp_bucket_name: str = os.getenv("GCP_BUCKET_NAME", "")
    gcp_raw_prefix: str = os.getenv("GCP_RAW_PREFIX", "raw/mvtec")
    gcp_model_prefix: str = os.getenv("GCP_MODEL_PREFIX", "models")
    local_data_dir: str = os.getenv("LOCAL_DATA_DIR", "data/raw/mvtec")
    local_model_dir: str = os.getenv("LOCAL_MODEL_DIR", "models")
    image_size: int = int(os.getenv("IMAGE_SIZE", "224"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "32"))
    epochs: int = int(os.getenv("EPOCHS", "5"))


settings = Settings()
