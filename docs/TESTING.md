# FastAPI Project Testing & Validation Setup Guide

## Objective

Implement an automated testing workflow for the **Family Tree FastAPI backend** so that:

1. Unit tests and API tests run automatically.
2. Tests execute before the application starts (similar to a deployment pipeline).
3. Tests use a **separate test database**.
4. Each test runs in isolation and **rolls back database changes**.
5. The container **stops if tests fail**.

This ensures reliability before the API is exposed.

---

# 1. Required Dependencies

Add the following to `requirements.txt`:

```
pytest
pytest-asyncio
httpx
fastapi[all]
```

These libraries enable:

* `pytest` → test runner
* `pytest-asyncio` → async FastAPI support
* `httpx` → API request testing
* `TestClient` → simulate API calls

---

# 2. Project Structure

The repository follows this structure:

```
family-tree
│
├── app
│   ├── main.py
│   ├── api          (auth, user_routes, person_routes, tree_routes, etc.)
│   ├── core         (config.py, database.py, security.py)
│   ├── models
│   ├── schemas
│   ├── services
│   └── repository
│
├── tests
│   ├── conftest.py
│   ├── test_health.py
│   └── test_auth.py
│
├── alembic
├── docker-compose.yml
├── entrypoint.sh
├── pytest.ini
└── requirements.txt
```

---

# 3. Configure Pytest

Create file:

`pytest.ini`

```
[pytest]
testpaths = tests
python_files = test_*.py
```

This tells pytest to automatically detect tests.

---

# 4. Test Database Setup

Use a **separate database** for testing.

Example `.env` configuration:

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/family_tree
TEST_DATABASE_URL=postgresql://postgres:postgres@db:5432/family_tree_test
```

`TEST_DATABASE_URL` is read from `app.core.config`. If unset, it falls back to `DATABASE_URL` (e.g. for local runs).

This prevents tests from affecting real data.

---

# 5. Testing Fixtures

Create file:

`tests/conftest.py`

Purpose:

* Create test database tables
* Provide database session for tests
* Rollback database changes after each test
* Provide API client

Example implementation (see `tests/conftest.py`):

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import TEST_DATABASE_URL
from app.models import user, person, relationship, occupation, address  # register all tables

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session(setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

Key Features:

* Each test runs in a **transaction**
* After test completion **rollback occurs**
* No test pollutes the database

---

# 6. Health Check Test

Create:

`tests/test_health.py`

```python
def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
```

This validates that the API server responds correctly.

---

# 7. Example API Test

Create:

`tests/test_auth.py`

```python
def test_register_user(client):
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
    assert "id" in data
```

This validates real API endpoints.

---

# 8. Running Tests Locally

Ensure `DATABASE_URL` or `TEST_DATABASE_URL` in `.env` points to a running PostgreSQL instance (e.g. `postgresql://user:pass@localhost:5432/family_tree_test`). Inside Docker, use `db` as host.

Run tests with:

```
pytest
```

Expected output:

```
tests/test_health.py .
tests/test_auth.py .

2 passed
```

---

# 9. Automated Testing Before API Startup

Modify `entrypoint.sh`.

Current deployment flow:

```
start container
→ run migrations
→ run tests
→ start API
```

Example implementation:

```
#!/bin/sh

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
alembic upgrade head || exit 1

echo "Running tests..."
pytest || exit 1

echo "Starting FastAPI server..."

uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Behavior:

If tests fail:

```
pytest FAILED
container stops
```

If tests pass:

```
API server starts
```

---

# 10. Running Full System

Start application:

```
docker compose up --build
```

Startup sequence:

```
database starts
↓
migrations run
↓
tests execute
↓
API server starts
```

---

# 11. Optional Professional Improvements

Future improvements for production-quality testing:

### 1. Testcontainers

Run a temporary PostgreSQL container for tests.

### 2. Load Testing

Use tools like:

```
locust
k6
```

### 3. CI Pipeline

Typical deployment pipeline:

```
Git Push
   ↓
Run Unit Tests
   ↓
Run API Tests
   ↓
Build Docker Image
   ↓
Deploy
```

Tools commonly used:

* GitHub Actions
* GitLab CI
* Jenkins

---

# Result

After implementing this setup:

* Every container start validates the application.
* APIs are automatically tested.
* Database corruption from tests is prevented.
* System behaves similarly to production deployment pipelines.
