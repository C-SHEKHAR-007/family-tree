"""Occupations API tests. All endpoints require auth."""

import uuid


def test_create_occupation_requires_auth(client, auth_headers):
    """POST /occupations/ returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    payload = {
        "person_id": str(person_id),
        "title": "Engineer",
        "company": "Acme",
    }
    response = client.post("/occupations/", json=payload)
    assert response.status_code == 401


def test_create_occupation_success(client, auth_headers):
    """POST /occupations/ creates occupation and returns 201."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    payload = {
        "person_id": str(person_id),
        "title": "Engineer",
        "company": "Acme",
    }
    response = client.post("/occupations/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Engineer"
    assert data["person_id"] == str(person_id)


def test_create_occupation_person_not_found(client, auth_headers):
    """POST /occupations/ with unknown person_id returns 404."""
    payload = {
        "person_id": str(uuid.uuid4()),
        "title": "Engineer",
    }
    response = client.post("/occupations/", json=payload, headers=auth_headers)
    assert response.status_code == 404


def test_get_occupation_requires_auth(client, auth_headers):
    """GET /occupations/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.get(f"/occupations/{occ_id}")
    assert response.status_code == 401


def test_get_occupation_not_found(client, auth_headers):
    """GET /occupations/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.get(f"/occupations/{some_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_occupation_success(client, auth_headers):
    """GET /occupations/{id} returns occupation when found."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.get(f"/occupations/{occ_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == occ_id


def test_get_occupations_by_person_requires_auth(client, auth_headers):
    """GET /occupations/person/{person_id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/occupations/person/{person_id}")
    assert response.status_code == 401


def test_get_occupations_by_person_success(client, auth_headers):
    """GET /occupations/person/{person_id} returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/occupations/person/{person_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_occupation_requires_auth(client, auth_headers):
    """PUT /occupations/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.put(
        f"/occupations/{occ_id}",
        json={"title": "Senior Engineer"},
    )
    assert response.status_code == 401


def test_update_occupation_success(client, auth_headers):
    """PUT /occupations/{id} updates and returns occupation."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.put(
        f"/occupations/{occ_id}",
        json={"title": "Senior Engineer"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Senior Engineer"


def test_delete_occupation_requires_auth(client, auth_headers):
    """DELETE /occupations/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.delete(f"/occupations/{occ_id}")
    assert response.status_code == 401


def test_delete_occupation_success(client, auth_headers):
    """DELETE /occupations/{id} returns 204."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/occupations/",
        json={"person_id": str(p.json()["id"]), "title": "Engineer"},
        headers=auth_headers,
    )
    occ_id = create.json()["id"]
    response = client.delete(f"/occupations/{occ_id}", headers=auth_headers)
    assert response.status_code == 204
