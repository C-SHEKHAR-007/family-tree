# Role Permissions Matrix

This document defines the complete role-based access control (RBAC) permissions for the Family Tree application.

---

## Available Roles

| Role | Description | Access Level |
|------|-------------|--------------|
| `SUPER_ADMIN` | Full system access, can manage all users and data | Highest |
| `FAMILY_ADMIN` | Can manage their family tree and administer family members | High |
| `admin` | Standard admin with full access | High |
| `member` | Can manage family tree data (create/edit) | Medium |
| `viewer` | Read-only access to view family data | Low |

---

## Permissions by Role

| Endpoint/Action | SUPER_ADMIN | FAMILY_ADMIN | admin | member | viewer |
|----------------|:-----------:|:------------:|:-----:|:------:|:------:|
| **Authentication** |
| Login | ✓ | ✓ | ✓ | ✓ | ✓ |
| Register | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get Profile | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Persons** |
| View all persons | ✓ | ✓ | ✓ | ✓ | ✓ |
| Search persons | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get person by ID | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create person | ✓ | ✓ | ✓ | ✓ | ✗ |
| Update person | ✓ | ✓ | ✓ | ✓ | ✗ |
| Delete person | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Relationships** |
| View relationships | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get family tree | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create relationship | ✓ | ✓ | ✓ | ✓ | ✗ |
| Delete relationship | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Family Tree** |
| Get ancestors | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get descendants | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get siblings | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Addresses** |
| View addresses | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create address | ✓ | ✓ | ✓ | ✓ | ✗ |
| Update address | ✓ | ✓ | ✓ | ✓ | ✗ |
| Delete address | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Occupations** |
| View occupations | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create occupation | ✓ | ✓ | ✓ | ✓ | ✗ |
| Update occupation | ✓ | ✓ | ✓ | ✓ | ✗ |
| Delete occupation | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Users** |
| Create user | ✓ | ✓ | ✓ | ✗ | ✗ |

---

## Summary by Access Type

| Permission Type | Roles Allowed |
|-----------------|---------------|
| **Admin Operations** (delete, create users) | `SUPER_ADMIN`, `FAMILY_ADMIN`, `admin` |
| **Write Operations** (create, update) | `SUPER_ADMIN`, `FAMILY_ADMIN`, `admin`, `member` |
| **Read Operations** (view, search) | All roles |

---

## HTTP Status Codes

| Scenario | Status Code |
|----------|-------------|
| Success | 200 / 201 / 204 |
| Unauthorized (no token) | 401 |
| Forbidden (insufficient role) | 403 |
| Not Found | 404 |

---

## Backend Implementation

### Security Dependencies (`app/core/security.py`)

```python
from app.core.security import (
    get_current_user,           # All authenticated users
    get_current_active_user,    # All active authenticated users
    admin_required,             # admin, SUPER_ADMIN, FAMILY_ADMIN only
    member_or_admin_required,   # Blocks viewers from write operations
    require_role,               # Custom role check factory
)
```

### Usage in Routes

```python
# Read operation - all authenticated users
@router.get("/persons/")
def get_persons(current_user: User = Depends(get_current_user)):
    ...

# Write operation - blocks viewers
@router.post("/persons/")
def create_person(current_user: User = Depends(member_or_admin_required)):
    ...

# Delete operation - admin only
@router.delete("/persons/{id}")
def delete_person(current_user: User = Depends(admin_required)):
    ...

# Custom role check
@router.delete("/users/{id}")
def delete_user(current_user: User = Depends(require_role(["SUPER_ADMIN"]))):
    ...
```

### Dependency Implementation

```python
def admin_required(current_user = Depends(get_current_user)):
    """Allows: admin, SUPER_ADMIN, FAMILY_ADMIN"""
    if current_user.role not in ["admin", "SUPER_ADMIN", "FAMILY_ADMIN"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def member_or_admin_required(current_user = Depends(get_current_user)):
    """Blocks viewers from write operations"""
    if current_user.role == "viewer":
        raise HTTPException(status_code=403, detail="Viewers have read-only access")
    return current_user

def require_role(allowed_roles: List[str]):
    """Factory for custom role requirements"""
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"Required role: {allowed_roles}")
        return current_user
    return role_checker
```

---

## Routes with Role Protection

### Person Routes (`app/api/person_routes.py`)
| Method | Endpoint | Protection |
|--------|----------|------------|
| GET | `/persons/` | `get_current_user` |
| GET | `/persons/{id}` | `get_current_user` |
| GET | `/persons/search` | `get_current_user` |
| POST | `/persons/` | `member_or_admin_required` |
| PUT | `/persons/{id}` | `member_or_admin_required` |
| DELETE | `/persons/{id}` | `admin_required` |

### Relationship Routes (`app/api/relationship_routes.py`)
| Method | Endpoint | Protection |
|--------|----------|------------|
| GET | `/relationships/` | `get_current_user` |
| GET | `/relationships/{id}` | `get_current_user` |
| POST | `/relationships/` | `member_or_admin_required` |
| DELETE | `/relationships/{id}` | `admin_required` |

### User Routes (`app/api/user_routes.py`)
| Method | Endpoint | Protection |
|--------|----------|------------|
| POST | `/users/` | `admin_required` |

### Address Routes (`app/api/address_routes.py`)
| Method | Endpoint | Protection |
|--------|----------|------------|
| GET | `/addresses/` | `get_current_active_user` |
| GET | `/addresses/{id}` | `get_current_active_user` |
| POST | `/addresses/` | `member_or_admin_required` |
| PUT | `/addresses/{id}` | `member_or_admin_required` |
| DELETE | `/addresses/{id}` | `admin_required` |

### Occupation Routes (`app/api/occupation_routes.py`)
| Method | Endpoint | Protection |
|--------|----------|------------|
| GET | `/occupations/` | `get_current_active_user` |
| GET | `/occupations/{id}` | `get_current_active_user` |
| POST | `/occupations/` | `member_or_admin_required` |
| PUT | `/occupations/{id}` | `member_or_admin_required` |
| DELETE | `/occupations/{id}` | `admin_required` |

---

## Role Hierarchy

```
SUPER_ADMIN (highest)
    ↓
FAMILY_ADMIN
    ↓
admin
    ↓
member
    ↓
viewer (lowest - read-only)
```

---

## Testing RBAC

The test fixtures provide two types of authentication headers:

```python
# Regular user (member role)
def test_example(client, auth_headers):
    response = client.post("/persons/", json=data, headers=auth_headers)
    assert response.status_code == 201  # Members can create

# Admin user
def test_example_admin(client, admin_headers):
    response = client.delete(f"/persons/{id}", headers=admin_headers)
    assert response.status_code == 204  # Admins can delete
```
