"""Family tree API tests. All require auth."""

import uuid


def test_get_ancestors_requires_auth(client, auth_headers):
    """GET /tree/{person_id}/ancestors returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/tree/{person_id}/ancestors")
    assert response.status_code == 401


def test_get_ancestors_success(client, auth_headers):
    """GET /tree/{person_id}/ancestors returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/tree/{person_id}/ancestors",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_ancestors_not_found(client, auth_headers):
    """GET /tree/{person_id}/ancestors returns 404 for unknown person."""
    some_id = uuid.uuid4()
    response = client.get(
        f"/tree/{some_id}/ancestors",
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_get_descendants_requires_auth(client, auth_headers):
    """GET /tree/{person_id}/descendants returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/tree/{person_id}/descendants")
    assert response.status_code == 401


def test_get_descendants_success(client, auth_headers):
    """GET /tree/{person_id}/descendants returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/tree/{person_id}/descendants",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_siblings_requires_auth(client, auth_headers):
    """GET /tree/{person_id}/siblings returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/tree/{person_id}/siblings")
    assert response.status_code == 401


def test_get_siblings_success(client, auth_headers):
    """GET /tree/{person_id}/siblings returns list."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/tree/{person_id}/siblings",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_full_tree_requires_auth(client, auth_headers):
    """GET /tree/{person_id}/full returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/tree/{person_id}/full")
    assert response.status_code == 401


def test_get_full_tree_success(client, auth_headers):
    """GET /tree/{person_id}/full returns tree structure."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/tree/{person_id}/full",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_get_tree_statistics_requires_auth(client, auth_headers):
    """GET /tree/{person_id}/statistics returns 401 without token."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(f"/tree/{person_id}/statistics")
    assert response.status_code == 401


def test_get_tree_statistics_success(client, auth_headers):
    """GET /tree/{person_id}/statistics returns stats dict."""
    p = client.post(
        "/persons/",
        json={"first_name": "P", "last_name": "P", "gender": "MALE"},
        headers=auth_headers,
    )
    person_id = p.json()["id"]
    response = client.get(
        f"/tree/{person_id}/statistics",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
