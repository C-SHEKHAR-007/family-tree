"""Persons API tests. All endpoints require auth; delete requires admin."""

import uuid

import pytest


def _person_payload(**overrides):
    return {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "MALE",
        "date_of_birth": None,
        "mobile": None,
        "email": None,
        "birth_place": None,
        **overrides,
    }


def test_create_person_requires_auth(client):
    """POST /persons/ returns 401 without token."""
    response = client.post("/persons/", json=_person_payload())
    assert response.status_code == 401


def test_create_person_success(client, auth_headers):
    """POST /persons/ creates person and returns 201."""
    response = client.post("/persons/", json=_person_payload(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["gender"] == "MALE"
    assert "id" in data


def test_get_all_persons_requires_auth(client):
    """GET /persons/ returns 401 without token."""
    response = client.get("/persons/")
    assert response.status_code == 401


def test_get_all_persons_success(client, auth_headers):
    """GET /persons/ returns list with pagination."""
    response = client.get("/persons/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_persons_pagination(client, auth_headers):
    """GET /persons/?skip=0&limit=10 respects query params."""
    response = client.get("/persons/?skip=0&limit=10", headers=auth_headers)
    assert response.status_code == 200


def test_search_persons_requires_auth(client):
    """GET /persons/search returns 401 without token."""
    response = client.get("/persons/search")
    assert response.status_code == 401


def test_search_persons_success(client, auth_headers):
    """GET /persons/search returns list."""
    response = client.get("/persons/search", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_person_requires_auth(client):
    """GET /persons/{id} returns 401 without token."""
    some_id = uuid.uuid4()
    response = client.get(f"/persons/{some_id}", headers={})
    assert response.status_code == 401


def test_get_person_not_found(client, auth_headers):
    """GET /persons/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.get(f"/persons/{some_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_person_success(client, auth_headers):
    """GET /persons/{id} returns person when found."""
    create = client.post("/persons/", json=_person_payload(), headers=auth_headers)
    assert create.status_code == 201
    person_id = create.json()["id"]
    response = client.get(f"/persons/{person_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == person_id


def test_update_person_requires_auth(client, auth_headers):
    """PUT /persons/{id} returns 401 without token."""
    create = client.post("/persons/", json=_person_payload(), headers=auth_headers)
    person_id = create.json()["id"]
    response = client.put(
        f"/persons/{person_id}",
        json={"first_name": "Jane"},
    )
    assert response.status_code == 401


def test_update_person_success(client, auth_headers):
    """PUT /persons/{id} updates and returns person."""
    create = client.post("/persons/", json=_person_payload(), headers=auth_headers)
    person_id = create.json()["id"]
    response = client.put(
        f"/persons/{person_id}",
        json={"first_name": "Jane", "last_name": "Doe"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"


def test_update_person_not_found(client, auth_headers):
    """PUT /persons/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.put(
        f"/persons/{some_id}",
        json={"first_name": "Jane"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_person_requires_admin(client, auth_headers):
    """DELETE /persons/{id} returns 403 for non-admin."""
    create = client.post("/persons/", json=_person_payload(), headers=auth_headers)
    person_id = create.json()["id"]
    response = client.delete(f"/persons/{person_id}", headers=auth_headers)
    assert response.status_code == 403


def test_delete_person_success(client, admin_headers, auth_headers):
    """DELETE /persons/{id} returns 204 for admin."""
    create = client.post("/persons/", json=_person_payload(), headers=admin_headers)
    person_id = create.json()["id"]
    response = client.delete(f"/persons/{person_id}", headers=admin_headers)
    assert response.status_code == 204


def test_delete_person_not_found(client, admin_headers):
    """DELETE /persons/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.delete(f"/persons/{some_id}", headers=admin_headers)
    assert response.status_code == 404
