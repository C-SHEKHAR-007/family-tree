"""Addresses API tests. All endpoints require auth."""

import uuid


def test_create_address_requires_auth(client, auth_headers):
    """POST /addresses/ returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    payload = {
        "person_id": str(person_id),
        "address_line": "123 Main St",
        "city": "City",
        "state": "State",
        "country": "Country",
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 401


def test_create_address_success(client, auth_headers):
    """POST /addresses/ creates address and returns 201."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    payload = {
        "person_id": str(person_id),
        "address_line": "123 Main St",
        "city": "City",
        "state": "State",
        "country": "Country",
    }
    response = client.post("/addresses/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["address_line"] == "123 Main St"
    assert data["person_id"] == str(person_id)


def test_create_address_person_not_found(client, auth_headers):
    """POST /addresses/ with unknown person_id returns 404."""
    payload = {
        "person_id": str(uuid.uuid4()),
        "address_line": "123 Main St",
    }
    response = client.post("/addresses/", json=payload, headers=auth_headers)
    assert response.status_code == 404


def test_get_address_requires_auth(client, auth_headers):
    """GET /addresses/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    pid = p.json()["id"]
    create = client.post(
        "/addresses/",
        json={"person_id": str(pid), "address_line": "123 Main"},
        headers=auth_headers,
    )
    addr_id = create.json()["id"]
    response = client.get(f"/addresses/{addr_id}")
    assert response.status_code == 401


def test_get_address_not_found(client, auth_headers):
    """GET /addresses/{id} returns 404 for unknown id."""
    some_id = uuid.uuid4()
    response = client.get(f"/addresses/{some_id}", headers=auth_headers)
    assert response.status_code == 404


def test_get_address_success(client, auth_headers):
    """GET /addresses/{id} returns address when found."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/addresses/",
        json={"person_id": str(p.json()["id"]), "address_line": "123 Main"},
        headers=auth_headers,
    )
    addr_id = create.json()["id"]
    response = client.get(f"/addresses/{addr_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == addr_id


def test_get_addresses_by_person_requires_auth(client, auth_headers):
    """GET /addresses/person/{person_id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/addresses/person/{person_id}")
    assert response.status_code == 401


def test_get_addresses_by_person_success(client, auth_headers):
    """GET /addresses/person/{person_id} returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/addresses/person/{person_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_address_requires_auth(client, auth_headers):
    """PUT /addresses/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/addresses/",
        json={"person_id": str(p.json()["id"]), "address_line": "123 Main"},
        headers=auth_headers,
    )
    addr_id = create.json()["id"]
    response = client.put(
        f"/addresses/{addr_id}",
        json={"address_line": "456 Other St"},
    )
    assert response.status_code == 401


def test_update_address_success(client, auth_headers):
    """PUT /addresses/{id} updates and returns address."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/addresses/",
        json={"person_id": str(p.json()["id"]), "address_line": "123 Main"},
        headers=auth_headers,
    )
    addr_id = create.json()["id"]
    response = client.put(
        f"/addresses/{addr_id}",
        json={"address_line": "456 Other St"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["address_line"] == "456 Other St"


def test_delete_address_requires_auth(client, auth_headers):
    """DELETE /addresses/{id} returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    create = client.post(
        "/addresses/",
        json={"person_id": str(p.json()["id"]), "address_line": "123 Main"},
        headers=auth_headers,
    )
    addr_id = create.json()["id"]
    response = client.delete(f"/addresses/{addr_id}")
    assert response.status_code == 401


def test_delete_address_success(client, admin_headers):
    """DELETE /addresses/{id} returns 204 for admin."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=admin_headers,
    )
    create = client.post(
        "/addresses/",
        json={"person_id": str(p.json()["id"]), "address_line": "123 Main"},
        headers=admin_headers,
    )
    addr_id = create.json()["id"]
    response = client.delete(f"/addresses/{addr_id}", headers=admin_headers)
    assert response.status_code == 204
