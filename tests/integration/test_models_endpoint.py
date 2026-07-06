"""
Integration tests for model registry API endpoint.
"""


def test_models_endpoint(client):
    response = client.get("/models")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
