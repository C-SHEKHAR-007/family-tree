# Family Tree Backend System

## Architecture & Implementation Reference Document

---

# 1. Project Overview

## 1.1 Purpose

The Family Tree Backend is a scalable authentication-enabled API system designed to:

* Manage users
* Support hierarchical family tree structures
* Provide secure login with JWT authentication
* Enforce role-based authorization
* Serve as a backend for a frontend client

---

# 2. Current Implementation Status

## ✅ Completed

### 2.1 Core Infrastructure

* SQLAlchemy database setup
* Declarative `Base`
* SessionLocal configuration
* Environment variable configuration via `.env`
* Clean project structure

### 2.2 Authentication System

* Password hashing using bcrypt via Passlib
* JWT token generation
* `.env` based SECRET_KEY configuration
* OAuth2 compatible login route
* Token payload includes:
  * `sub` (user id)
  * `email`
  * `role`
  * `exp`

### 2.3 Login API

<pre class="overflow-visible! px-0!" data-start="1219" data-end="1243"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>POST /auth/login</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

* Uses OAuth2PasswordRequestForm
* Returns:
  <pre class="overflow-visible! px-0!" data-start="1291" data-end="1362"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "access_token": "...",</span><br/><span>  "token_type": "bearer"</span><br/><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>
* Returns 401 for invalid credentials
* Production-ready JWT structure

### 2.4 Repository Pattern

* `user_repo.py`
* DB logic separated from route logic

### 2.5 Clean Separation of Concerns

| Layer      | Responsibility             |
| ---------- | -------------------------- |
| core       | Security, config, database |
| models     | DB models                  |
| repository | DB access logic            |
| schemas    | Request/Response models    |
| api/routes | API endpoints              |
| main       | Application bootstrap      |

---

# 3. High-Level System Design (HLD)

## 3.1 Architecture Pattern

Layered Monolithic Architecture

<pre class="overflow-visible! px-0!" data-start="1911" data-end="2007"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Client</span><br/><span>  ↓</span><br/><span>FastAPI Routes</span><br/><span>  ↓</span><br/><span>Service / Repository Layer</span><br/><span>  ↓</span><br/><span>SQLAlchemy ORM</span><br/><span>  ↓</span><br/><span>Database</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Benefits

* Clean separation
* Easily scalable
* Future microservice-ready
* Testable

---

## 3.2 Authentication Flow (High Level)

<pre class="overflow-visible! px-0!" data-start="2145" data-end="2368"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>User → /auth/login</span><br/><span>      → Validate credentials</span><br/><span>      → Generate JWT</span><br/><span>      → Return token</span><br/><span>      → Client stores token</span><br/><span>      → Token sent in Authorization header</span><br/><span>      → Backend validates token</span><br/><span>      → Access granted</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## 3.3 Authorization Strategy

Current plan:

* Role stored in JWT
* Role field in User table
* Future:
  * Admin-only routes
  * Role-based dependency guards

---

# 4. Low-Level Design (LLD)

---

## 4.1 User Model (Core Identity)

### Fields

* id (UUID)
* email (unique)
* password_hash
* role
* created_at
* updated_at

### Relationships

* May link to:
  * Person
  * Family Tree

---

## 4.2 Security Layer

### Password Hashing

* Passlib bcrypt
* Hash stored in DB
* Plain password never stored

### JWT Structure

<pre class="overflow-visible! px-0!" data-start="2898" data-end="3001"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "sub": </span><span class="ͼr">"user_id"</span><span>,</span><br/><span>  "email": </span><span class="ͼr">"user@email.com"</span><span>,</span><br/><span>  "role": </span><span class="ͼr">"admin"</span><span>,</span><br/><span>  "exp": </span><span class="ͼq">1700000000</span><br/><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Token Expiration

* Controlled via `.env`
* Default: 60 minutes

---

## 4.3 Environment Configuration

`.env` contains:

<pre class="overflow-visible! px-0!" data-start="3128" data-end="3208"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>SECRET_KEY=</span><br/><span>ALGORITHM=HS256</span><br/><span>ACCESS_TOKEN_EXPIRE_MINUTES=60</span><br/><span>DATABASE_URL=</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Loaded via `config.py`.

No secrets are hardcoded.

---

# 5. Folder Structure Reference

<pre class="overflow-visible! px-0!" data-start="3300" data-end="3633"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>app/</span><br/><span> ├── api/</span><br/><span> │    └── routes/</span><br/><span> │         └── auth.py</span><br/><span> ├── core/</span><br/><span> │    ├── config.py</span><br/><span> │    ├── database.py</span><br/><span> │    └── security.py</span><br/><span> ├── models/</span><br/><span> │    ├── user.py</span><br/><span> │    ├── person.py</span><br/><span> │    └── __init__.py</span><br/><span> ├── repository/</span><br/><span> │    └── user_repo.py</span><br/><span> ├── schemas/</span><br/><span> │    └── auth_schema.py</span><br/><span> └── main.py</span><br/><span>scripts/</span><br/><span> └── create_admin.py</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6. What Will Be Implemented Next

## 6.1 Immediate Next Steps

### 🔐 1. Protected Routes

Add:

<pre class="overflow-visible! px-0!" data-start="3739" data-end="3759"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>GET /auth/me</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Using:

<pre class="overflow-visible! px-0!" data-start="3769" data-end="3795"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>get_current_user()</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

JWT decoding + DB fetch.

---

### 🛡 2. Role-Based Access Control (RBAC)

Add:

* `admin_required` dependency
* Role validation from token
* Route guards

---

### 🔄 3. Refresh Token System

Add:

* Access token (short-lived)
* Refresh token (long-lived)
* Token rotation

---

### 👤 4. User Registration Endpoint

<pre class="overflow-visible! px-0!" data-start="4115" data-end="4142"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>POST /auth/register</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

With:

* Email validation
* Duplicate email prevention
* Password strength check

---

### 🌳 5. Family Tree Core Logic

* Create family root
* Add person
* Define relationships
* Recursive queries

---

### 📊 6. Relationship Graph Design

Will support:

* Parent-child
* Siblings
* Spouse
* Generational queries
* Tree traversal

Likely using adjacency list pattern in SQL.

---

# 7. Security Roadmap

Future improvements:

* Token blacklist (logout support)
* Rate limiting login
* Account lock after failed attempts
* Email verification
* Password reset flow
* HTTPS enforcement
* CORS configuration tightening

---

# 8. Scalability Considerations

### Current State

Single service monolith.

### Designed for:

* Horizontal scaling
* Stateless authentication (JWT)
* Microservice separation later

Possible future separation:

* Auth service
* Family tree service
* Notification service

---

# 9. Database Strategy

Current:

* SQLAlchemy ORM

Planned:

* Alembic migrations
* Indexed email field
* Indexed foreign keys
* UUID primary keys

---

# 10. Design Principles Followed

* Separation of concerns
* Repository pattern
* Dependency injection
* Environment-based config
* JWT stateless authentication
* Clean layered architecture

---

# 11. Development Guidelines (For Copilot Use)

When extending:

### Always:

* Keep DB logic in repository layer
* Keep business logic out of routes
* Never hardcode secrets
* Use dependency injection
* Keep schemas separate from models

### Never:

* Access DB directly in routes
* Mix JWT logic inside models
* Put config values inline
* Store plain passwords

---

# 12. Current System Maturity Level

Authentication: ✅ Production Ready

Authorization: 🔄 In Progress

Family Tree Logic: 🟡 Partially Designed

Advanced Security: ⏳ Planned

---

# 13. Long-Term Vision

This system should evolve into:

* Enterprise-ready auth backend
* Role-based hierarchical data engine
* Multi-tenant family tree system
* API-first scalable architecture

---

# 14. Summary

You now have:

* Clean architecture
* Proper authentication
* Secure token generation
* Production-grade config handling
* Strong foundation for RBAC

The backend foundation is correctly structured.
