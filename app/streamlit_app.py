import streamlit as st
from src.config import settings
from src.preprocess import summarize_dataset

st.set_page_config(page_title="Industrial Defect Detection", layout="wide")

st.title("Industrial Defect Detection")
st.caption("Stage 1: GitHub-ready scaffold with GCP, Docker, TensorFlow, and PyTorch placeholders.")

st.header("Project Status")
st.write(
    "This first version sets up the repository structure, Docker environment, "
    "GCP configuration, and Streamlit shell. Model training will be added in stages."
)

st.header("Configuration")
st.json({
    "bucket": settings.gcp_bucket_name or "not configured",
    "raw_prefix": settings.gcp_raw_prefix,
    "local_data_dir": settings.local_data_dir,
    "image_size": settings.image_size,
    "batch_size": settings.batch_size,
    "epochs": settings.epochs,
})

st.header("Local Dataset Summary")
summary = summarize_dataset(settings.local_data_dir)
if summary:
    st.dataframe(summary, use_container_width=True)
else:
    st.info("No local dataset found yet. Upload MVTec AD to GCS, then download it in Stage 2.")
