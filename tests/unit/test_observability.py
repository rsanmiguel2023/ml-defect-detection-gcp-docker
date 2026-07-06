"""
Unit tests for observability middleware.
"""


def test_request_id_header_is_returned(client):
    response = client.get("/health", headers={"X-Request-ID": "test-request-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"


def test_request_id_is_generated_when_missing(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]
