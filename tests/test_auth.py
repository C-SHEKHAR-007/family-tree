"""Authentication API tests."""


def test_register_user(client):
    """POST /auth/register creates a user and returns 201."""
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@test.com",
        "username": "testuser",
        "password": "password123",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client):
    """Register with existing email returns 400."""
    payload = {
        "first_name": "First",
        "last_name": "User",
        "email": "same@test.com",
        "username": "user1",
        "password": "password123",
    }
    client.post("/auth/register", json=payload)
    payload2 = {
        "first_name": "Second",
        "last_name": "User",
        "email": "same@test.com",
        "username": "user2",
        "password": "otherpass",
    }
    response = client.post("/auth/register", json=payload2)
    assert response.status_code == 400
    assert "email" in response.json().get("detail", "").lower()


def test_login(client):
    """POST /auth/login returns token for valid credentials."""
    payload = {
        "first_name": "Login",
        "last_name": "User",
        "email": "login@test.com",
        "username": "loginuser",
        "password": "secret123",
    }
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_invalid_password(client):
    """POST /auth/login returns 401 for wrong password."""
    payload = {
        "first_name": "Login",
        "last_name": "User",
        "email": "badlogin@test.com",
        "username": "badlogin",
        "password": "secret123",
    }
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        data={"username": "badlogin@test.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_register_duplicate_username(client):
    """Register with existing username returns 400."""
    payload = {
        "first_name": "First",
        "last_name": "User",
        "email": "first@test.com",
        "username": "sameuser",
        "password": "password123",
    }
    client.post("/auth/register", json=payload)
    payload2 = {
        "first_name": "Second",
        "last_name": "User",
        "email": "second@test.com",
        "username": "sameuser",
        "password": "otherpass",
    }
    response = client.post("/auth/register", json=payload2)
    assert response.status_code == 400
    assert "username" in response.json().get("detail", "").lower()


def test_get_me(client, auth_headers):
    """GET /auth/me returns current user profile when authenticated."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth@test.com"
    assert data["username"] == "authuser"


def test_get_me_unauthorized(client):
    """GET /auth/me returns 401 without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401
