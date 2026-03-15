"""Users API tests. POST /users/ requires auth."""

import pytest


def test_create_user_requires_auth(client):
    """POST /users/ returns 401 without token."""
    payload = {
        "first_name": "New",
        "last_name": "User",
        "email": "new@test.com",
        "username": "newuser",
        "password": "password123",
        "role": "member",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 401


def test_create_user_success(client, admin_headers):
    """POST /users/ creates user and returns 200 when authenticated as admin."""
    payload = {
        "first_name": "Created",
        "last_name": "User",
        "email": "created@test.com",
        "username": "createduser",
        "mobile": None,
        "password": "password123",
        "role": "member",
    }
    response = client.post("/users/", json=payload, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "created@test.com"
    assert data["username"] == "createduser"
    assert "id" in data
    assert "password" not in data
