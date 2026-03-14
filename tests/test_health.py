"""Health check API tests."""


def test_health(client):
    """Root endpoint returns 200 and healthy status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "message" in data
