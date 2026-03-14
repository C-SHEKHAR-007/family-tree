"""Relationships API tests. All require auth; delete endpoints require admin."""

import uuid

import pytest


def test_create_relationship_requires_auth(client, auth_headers):
    """POST /relationships/ returns 401 without token."""
    # Create two persons first (need valid UUIDs)
    p1 = client.post(
        "/persons/",
        json={
            "first_name": "A",
            "last_name": "Person",
            "gender": "MALE",
        },
        headers=auth_headers,
    )
    p2 = client.post(
        "/persons/",
        json={
            "first_name": "B",
            "last_name": "Person",
            "gender": "FEMALE",
        },
        headers=auth_headers,
    )
    person_id = p1.json()["id"]
    related_id = p2.json()["id"]
    payload = {
        "person_id": str(person_id),
        "related_person_id": str(related_id),
        "relationship_type": "SPOUSE",
    }
    response = client.post("/relationships/", json=payload)
    assert response.status_code == 401


def test_create_relationship_success(client, auth_headers):
    """POST /relationships/ creates relationship and returns 201."""
    p1 = client.post(
        "/persons/",
        json={"first_name": "Dad", "last_name": "X", "gender": "MALE"},
        headers=auth_headers,
    )
    p2 = client.post(
        "/persons/",
        json={"first_name": "Mom", "last_name": "X", "gender": "FEMALE"},
        headers=auth_headers,
    )
    person_id = p1.json()["id"]
    related_id = p2.json()["id"]
    payload = {
        "person_id": str(person_id),
        "related_person_id": str(related_id),
        "relationship_type": "SPOUSE",
    }
    response = client.post("/relationships/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["person_id"] == str(person_id)
    assert data["related_person_id"] == str(related_id)
    assert data["relationship_type"] == "SPOUSE"


def test_get_all_relationships_requires_auth(client):
    """GET /relationships/ returns 401 without token."""
    response = client.get("/relationships/")
    assert response.status_code == 401


def test_get_all_relationships_success(client, auth_headers):
    """GET /relationships/ returns list."""
    response = client.get("/relationships/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_relationship_requires_auth(client, auth_headers):
    """GET /relationships/{id} returns 401 without token."""
    rel = client.post(
        "/relationships/",
        json={
            "person_id": str(uuid.uuid4()),
            "related_person_id": str(uuid.uuid4()),
            "relationship_type": "SIBLING",
        },
        headers=auth_headers,
    )
    if rel.status_code != 201:
        pytest.skip("Need valid relationship (persons may not exist)")
    rid = rel.json()["id"]
    response = client.get(f"/relationships/{rid}")
    assert response.status_code == 401


def test_get_relationship_not_found(client, auth_headers):
    """GET /relationships/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.get(f"/relationships/{some_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_relationship_success(client, auth_headers):
    """GET /relationships/{id} returns relationship when found."""
    p1 = client.post(
        "/persons/",
        json={"first_name": "A", "last_name": "A", "gender": "MALE"},
        headers=auth_headers,
    )
    p2 = client.post(
        "/persons/",
        json={"first_name": "B", "last_name": "B", "gender": "FEMALE"},
        headers=auth_headers,
    )
    rel = client.post(
        "/relationships/",
        json={
            "person_id": str(p1.json()["id"]),
            "related_person_id": str(p2.json()["id"]),
            "relationship_type": "SPOUSE",
        },
        headers=auth_headers,
    )
    assert rel.status_code == 201
    rid = rel.json()["id"]
    response = client.get(f"/relationships/{rid}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == rid


def test_get_person_relationships_requires_auth(client, auth_headers):
    """GET /relationships/person/{person_id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/relationships/person/{person_id}")
    assert response.status_code == 401


def test_get_person_relationships_success(client, auth_headers):
    """GET /relationships/person/{person_id} returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/relationships/person/{person_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_person_family_requires_auth(client, auth_headers):
    """GET /relationships/person/{person_id}/family returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/relationships/person/{person_id}/family")
    assert response.status_code == 401


def test_get_person_family_success(client, auth_headers):
    """GET /relationships/person/{person_id}/family returns family structure."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/relationships/person/{person_id}/family",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "person_id" in data
    assert data["person_id"] == str(person_id)


def test_delete_relationship_requires_admin(client, auth_headers):
    """DELETE /relationships/{id} returns 403 for non-admin."""
    p1 = client.post(
        "/persons/",
        json={"first_name": "X", "last_name": "X", "gender": "MALE"},
        headers=auth_headers,
    )
    p2 = client.post(
        "/persons/",
        json={"first_name": "Y", "last_name": "Y", "gender": "FEMALE"},
        headers=auth_headers,
    )
    rel = client.post(
        "/relationships/",
        json={
            "person_id": p1.json()["id"],
            "related_person_id": p2.json()["id"],
            "relationship_type": "SPOUSE",
        },
        headers=auth_headers,
    )
    if rel.status_code != 201:
        pytest.skip("Create relationship failed")
    rid = rel.json()["id"]
    response = client.delete(f"/relationships/{rid}", headers=auth_headers)
    assert response.status_code == 403


def test_delete_relationship_success(client, admin_headers):
    """DELETE /relationships/{id} returns 204 for admin."""
    p1 = client.post(
        "/persons/",
        json={"first_name": "A", "last_name": "A", "gender": "MALE"},
        headers=admin_headers,
    )
    p2 = client.post(
        "/persons/",
        json={"first_name": "B", "last_name": "B", "gender": "FEMALE"},
        headers=admin_headers,
    )
    rel = client.post(
        "/relationships/",
        json={
            "person_id": p1.json()["id"],
            "related_person_id": p2.json()["id"],
            "relationship_type": "SPOUSE",
        },
        headers=admin_headers,
    )
    assert rel.status_code == 201
    rid = rel.json()["id"]
    response = client.delete(f"/relationships/{rid}", headers=admin_headers)
    assert response.status_code == 204
