# Family Tree API

A FastAPI backend for managing family trees, people, relationships, addresses, and occupations, with JWT-based authentication and role-based access control (RBAC).  
Includes a full pytest-based test suite and Dockerized deployment.

---

### 1. Features

- **Authentication & Authorization**
  - User registration and login with JWT tokens
  - Protected routes using `Bearer` tokens
  - Role-based access (`admin` vs regular users)

- **Core Domain**
  - `User` accounts linked to `Person` records
  - `Person` entities with gender, contact details, and birth place
  - `Relationship` entities (FATHER, MOTHER, SPOUSE, CHILD, SIBLING)
  - `Address` records per person
  - `Occupation` records per person

- **Family Tree Operations**
  - Ancestors and descendants traversal
  - Siblings and full tree views
  - Tree statistics (counts, depths, etc.)

- **Tooling**
  - SQLAlchemy 2.x + Alembic migrations
  - Pytest suite covering all API routes
  - Dockerfile + docker-compose for local/dev usage

---

### 2. Tech Stack

- **Language**: Python 3.11+ (you’re using 3.13 locally)
- **Framework**: FastAPI
- **Web server**: Uvicorn
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Auth**: JWT (python-jose), bcrypt via passlib
- **Settings**: Pydantic Settings / `.env`
- **Testing**: pytest, httpx, FastAPI `TestClient`
- **Container**: Docker, docker-compose

---

### 3. Project Structure

```text
Family-Tree/
│
├── app/
│   ├── main.py                # FastAPI app & router registration
│   ├── api/                   # Route modules (auth, users, persons, etc.)
│   │   ├── auth.py
│   │   ├── user_routes.py
│   │   ├── person_routes.py
│   │   ├── relationship_routes.py
│   │   ├── tree_routes.py
│   │   ├── address_routes.py
│   │   └── occupation_routes.py
│   ├── core/                  # Core infrastructure
│   │   ├── config.py          # Settings (SECRET_KEY, DATABASE_URL, TEST_DATABASE_URL, etc.)
│   │   ├── database.py        # SQLAlchemy Base, SessionLocal, get_db()
│   │   └── security.py        # Password hashing, JWT, oauth2, role helpers
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic models
│   ├── repository/            # DB access layer
│   └── services/              # Business logic (user_service, person_service, etc.)
│
├── tests/
│   ├── conftest.py            # Test DB engine, fixtures, auth/admin headers
│   ├── test_health.py         # GET /
│   ├── test_auth.py           # /auth endpoints
│   ├── test_users.py          # /users endpoints
│   ├── test_persons.py        # /persons endpoints
│   ├── test_relationships.py  # /relationships endpoints
│   ├── test_tree.py           # /tree endpoints
│   ├── test_addresses.py      # /addresses endpoints
│   └── test_occupations.py    # /occupations endpoints
│
├── alembic/                   # Migration env & versions
├── alembic.ini
├── entrypoint.sh              # Container entrypoint (migrations + tests + API)
├── docker-compose.yml         # App + Postgres
├── Dockerfile
├── requirements.txt
├── pytest.ini                 # pytest config (testpaths, pythonpath)
├── .env                       # Environment variables (local/dev)
└── docs/
    └── TESTING.md             # Detailed testing guide


## 4. Configuration

All configuration is provided via a `.env` file and read in `app/core/config.py`.

### Example `.env`

```env
# Security
SECRET_KEY=your-very-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Main application DB
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/family_tree

# Test database (used by pytest)
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/family_tree_test
```

### Values exposed by `config.py`

The configuration module exposes the following variables:

* `SECRET_KEY`
* `ALGORITHM`
* `ACCESS_TOKEN_EXPIRE_MINUTES`
* `DATABASE_URL`
* `TEST_DATABASE_URL` (falls back to `DATABASE_URL` if unset)

---

## 5. Running the Application (Local)

### 5.1 Install Dependencies

Create a virtual environment (recommended) and install dependencies:

```bash
cd Family-Tree
pip install -r requirements.txt
```

If you encounter **bcrypt / passlib issues**, pin bcrypt to a compatible version:

```bash
pip install "bcrypt>=4.0,<4.1"
```

---

### 5.2 Start PostgreSQL

Ensure PostgreSQL is running and matches the `DATABASE_URL`.

Create the main database:

```sql
CREATE DATABASE family_tree;
```

---

### 5.3 Run Migrations

Apply database migrations using Alembic:

```bash
alembic upgrade head
```

---

### 5.4 Start the FastAPI Application

Run the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc
* **Health Check:** `GET /` → `{"status": "healthy", ...}`

---

## 6. Running the Application (Docker)

Build and start the containers:

```bash
docker compose up --build
```

### Container Startup Behavior

The default `entrypoint.sh` performs the following steps:

1. Waits for the database to become available.
2. Runs database migrations:

```bash
alembic upgrade head
```

3. Executes tests:

```bash
pytest
```

4. Starts the FastAPI server **only if tests pass**.

If tests fail, the container exits with a **non-zero exit code**, which is safe for CI/CD pipelines.

---

## 7. Testing

### 7.1 Test Database

Tests use `TEST_DATABASE_URL` from the `.env` file.

Behavior:

* `tests/conftest.py` automatically **creates the test database** (e.g., `family_tree_test`) if it does not exist.
* All tables are created **once per test session** and dropped afterward.
* Each test runs inside a **database transaction**, which is **rolled back after the test**, keeping the database clean.

---

### 7.2 Fixtures

Key fixtures defined in `tests/conftest.py`:

| Fixture          | Purpose                                                                |
| ---------------- | ---------------------------------------------------------------------- |
| `setup_database` | Creates and drops tables for the test database                         |
| `db_session`     | Provides a transactional SQLAlchemy session (rollback after each test) |
| `client`         | FastAPI `TestClient` with `get_db` overridden to use the test session  |
| `auth_headers`   | Registers a normal user and returns `Authorization: Bearer <token>`    |
| `admin_headers`  | Creates an admin user in the DB and logs in to obtain an admin JWT     |

---

### 7.3 Running Tests

Run tests from the project root:

```bash
pytest
```

Verbose mode:

```bash
pytest tests/ -v
```

Run a specific test module:

```bash
pytest tests/test_auth.py -v
```

When running inside **Docker**, tests are automatically executed by `entrypoint.sh`.

---

## 8. API Overview

### 8.1 Authentication (`/auth`)

| Endpoint              | Description                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| `POST /auth/register` | Register a new user                                                     |
| `POST /auth/login`    | Obtain JWT access token (OAuth2 password flow; username field is email) |
| `GET /auth/me`        | Get current user profile (requires Authorization header)                |

---

### 8.2 Users (`/users`)

| Endpoint       | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| `POST /users/` | Create a user (admin / authorized calls via `user_service`) |

---

### 8.3 Persons (`/persons`)

All endpoints require authentication.

| Endpoint               | Description                                    |
| ---------------------- | ---------------------------------------------- |
| `POST /persons/`       | Create person                                  |
| `GET /persons/`        | List persons with pagination (`skip`, `limit`) |
| `GET /persons/search`  | Search by first name, last name, gender        |
| `GET /persons/{id}`    | Get person by ID                               |
| `PUT /persons/{id}`    | Update person                                  |
| `DELETE /persons/{id}` | Delete person (**admin only**)                 |

---

### 8.4 Relationships (`/relationships`)

All endpoints require authentication; some require admin privileges.

| Endpoint                                                        | Description                                                       |
| --------------------------------------------------------------- | ----------------------------------------------------------------- |
| `POST /relationships/`                                          | Create relationship (auto inverse relationships when appropriate) |
| `GET /relationships/`                                           | List relationships with pagination                                |
| `GET /relationships/{id}`                                       | Get relationship by ID                                            |
| `GET /relationships/person/{person_id}`                         | List relationships for a person                                   |
| `GET /relationships/person/{person_id}/family`                  | Structured family view                                            |
| `DELETE /relationships/{id}`                                    | Delete relationship (**admin**)                                   |
| `DELETE /relationships/between/{person_id}/{related_person_id}` | Delete relationship between two people (**admin**)                |

---

### 8.5 Tree (`/tree`)

All endpoints require authentication.

| Endpoint                                        | Description         |
| ----------------------------------------------- | ------------------- |
| `GET /tree/{person_id}/ancestors?max_depth=5`   | Fetch ancestors     |
| `GET /tree/{person_id}/descendants?max_depth=5` | Fetch descendants   |
| `GET /tree/{person_id}/siblings`                | Fetch siblings      |
| `GET /tree/{person_id}/full?depth=3`            | Full tree structure |
| `GET /tree/{person_id}/statistics`              | Tree statistics     |

---

### 8.6 Addresses (`/addresses`)

Require an active user.

| Endpoint                            | Description               |
| ----------------------------------- | ------------------------- |
| `POST /addresses/`                  | Create address            |
| `GET /addresses/{id}`               | Get address               |
| `GET /addresses/person/{person_id}` | Get addresses of a person |
| `PUT /addresses/{id}`               | Update address            |
| `DELETE /addresses/{id}`            | Delete address            |

---

### 8.7 Occupations (`/occupations`)

Require an active user.

| Endpoint                              | Description                 |
| ------------------------------------- | --------------------------- |
| `POST /occupations/`                  | Create occupation           |
| `GET /occupations/{id}`               | Get occupation              |
| `GET /occupations/person/{person_id}` | Get occupations of a person |
| `PUT /occupations/{id}`               | Update occupation           |
| `DELETE /occupations/{id}`            | Delete occupation           |

---

## 9. Development Notes

* **Pydantic v2:** Schemas use `from_attributes = True`, and services use `.model_dump()` instead of `.dict()` where required.
* **bcrypt & passlib:** If errors appear such as
  `ValueError: password cannot be longer than 72 bytes` or
  `module 'bcrypt' has no attribute '__about__'`, pin bcrypt:

```bash
pip install "bcrypt>=4.0,<4.1"
```

* **Testing before deploy:** Because the Docker entrypoint runs tests before starting the server, failing tests will prevent the API from starting in CI/CD or staging environments. This is intentional to ensure stability.

---

## 10. Future Improvements

Possible enhancements for the project:

* Add **consistent pagination and filtering** across all list endpoints.
* Implement **soft delete and auditing** for critical entities.
* Expand **RBAC roles** (e.g., `FAMILY_ADMIN`, `SUPER_ADMIN`).
* Introduce **load and stress testing** using tools like `k6` or `locust`.
* Add **GitHub Actions / CI pipeline** for automated testing and Docker builds.
