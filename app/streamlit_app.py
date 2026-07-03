"""
Streamlit dashboard for industrial defect detection.
"""

import requests
import streamlit as st

API_BASE_URL = "http://api:8000"

CATEGORIES = [
    "bottle",
    "cable",
    "capsule",
    "carpet",
    "grid",
    "hazelnut",
    "leather",
    "metal_nut",
    "pill",
    "screw",
    "tile",
    "toothbrush",
    "transistor",
    "wood",
    "zipper",
]


def get_available_models():
    try:
        response = requests.get(f"{API_BASE_URL}/models", timeout=30)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return {}

    return {}


st.set_page_config(
    page_title="Industrial Defect Detection",
    layout="centered",
)

st.title("Industrial Defect Detection")
st.write("TensorFlow and PyTorch defect detection using MVTec AD.")

models = get_available_models()

mode = st.radio(
    "Mode",
    ["Single Prediction", "Batch Prediction", "Evaluate Model"],
)

framework = st.selectbox(
    "Framework",
    ["tensorflow", "pytorch"],
)

category = st.selectbox(
    "MVTec Category",
    CATEGORIES,
)

available_versions = models.get(framework, {}).get(category, [])

if available_versions:
    model_version = st.selectbox(
        "Model Version",
        ["latest"] + available_versions,
    )
else:
    model_version = "latest"
    st.warning("No saved model versions found yet for this framework/category.")

if mode == "Single Prediction":
    uploaded_file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        if st.button("Predict"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            data = {
                "framework": framework,
                "category": category,
                "model_version": model_version,
            }

            response = requests.post(
                f"{API_BASE_URL}/predict",
                files=files,
                data=data,
                timeout=60,
            )

            if response.status_code == 200:
                result = response.json()

                st.success(f"Prediction: {result['prediction']}")
                st.metric("Confidence", f"{result['confidence']:.2%}")
                st.write(f"Model Version: {result['model_version']}")
            else:
                st.error(response.text)

elif mode == "Batch Prediction":
    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        if st.button("Run Batch Prediction"):
            files = [
                (
                    "files",
                    (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    ),
                )
                for uploaded_file in uploaded_files
            ]

            data = {
                "framework": framework,
                "category": category,
                "model_version": model_version,
            }

            response = requests.post(
                f"{API_BASE_URL}/predict-batch",
                files=files,
                data=data,
                timeout=120,
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Batch prediction completed.")
                st.write(f"Model Version: {result['model_version']}")
                st.dataframe(result["results"])
            else:
                st.error(response.text)

else:
    if st.button("Run Evaluation"):
        data = {
            "framework": framework,
            "category": category,
        }

        response = requests.post(
            f"{API_BASE_URL}/evaluate",
            data=data,
            timeout=300,
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Evaluation completed.")
            st.json(result)
        else:
            st.error(response.text)
