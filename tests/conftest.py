"""
Pytest fixtures for Family Tree API tests.

- Uses a separate test database (TEST_DATABASE_URL).
- Creates the test database if it does not exist.
- Each test runs in a transaction that is rolled back after the test.
- Provides TestClient with get_db overridden to use the test session.
"""
import re
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import TEST_DATABASE_URL

# Import all models so Base.metadata contains every table
from app.models import user, person, relationship, occupation, address  # noqa: F401


def _ensure_test_database_exists():
    """Create the test database if it does not exist (PostgreSQL)."""
    parsed = urlparse(TEST_DATABASE_URL)
    if parsed.scheme not in ("postgresql", "postgres"):
        return
    dbname = (parsed.path or "").lstrip("/").split("?")[0]
    if not dbname or not re.match(r"^[a-zA-Z0-9_]+$", dbname):
        return
    # Connect to default 'postgres' database to run CREATE DATABASE
    admin_path = f"/postgres" + (f"?{parsed.query}" if parsed.query else "")
    admin_url = parsed._replace(path=admin_path).geturl()
    if admin_url.startswith("postgres://"):
        admin_url = admin_url.replace("postgres://", "postgresql://", 1)
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        r = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": dbname})
        if r.scalar() is None:
            conn.execute(text(f'CREATE DATABASE "{dbname}"'))
    admin_engine.dispose()


_ensure_test_database_exists()

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def setup_database():
    """Create all tables for the test run; drop after session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_database):
    """Provide a DB session inside a transaction; rollback after test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """Provide TestClient with get_db overridden to use test session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    """Register a user, login, and return Authorization headers."""
    payload = {
        "first_name": "Auth",
        "last_name": "User",
        "email": "auth@test.com",
        "username": "authuser",
        "password": "authpass123",
    }
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        data={"username": "auth@test.com", "password": "authpass123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_headers(db_session, client):
    """Create an admin user in DB, login, and return Authorization headers."""
    import uuid
    from app.models.user import User
    from app.core.security import hash_password

    admin = User(
        id=uuid.uuid4(),
        first_name="Admin",
        last_name="User",
        email="admin@test.com",
        username="adminuser",
        password_hash=hash_password("adminpass123"),
        role="admin",
    )
    db_session.add(admin)
    db_session.flush()

    response = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "adminpass123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
