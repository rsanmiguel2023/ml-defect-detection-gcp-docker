"""
Integration tests for observability endpoints.
"""


def test_metrics_endpoint(client):
    response = client.get("/metrics")

    assert response.status_code == 200

    payload = response.json()

    assert "cached_models" in payload
    assert "cache_hits" in payload
    assert "cache_misses" in payload


def test_cache_endpoint(client):
    response = client.get("/cache")

    assert response.status_code == 200

    payload = response.json()

    assert "cached_models" in payload
    assert "cache_hits" in payload
    assert "cache_misses" in payload
    assert "cache_keys" in payload
