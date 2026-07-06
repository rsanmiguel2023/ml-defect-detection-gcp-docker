"""
Integration tests for prediction endpoint validation paths.
"""


def test_predict_rejects_missing_file(client):
    response = client.post(
        "/predict",
        data={
            "framework": "tensorflow",
            "category": "bottle",
            "model_version": "latest",
        },
    )

    assert response.status_code == 422


def test_predict_batch_rejects_missing_files(client):
    response = client.post(
        "/predict-batch",
        data={
            "framework": "tensorflow",
            "category": "bottle",
            "model_version": "latest",
        },
    )

    assert response.status_code == 422
