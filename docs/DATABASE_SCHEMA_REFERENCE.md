## Database Schema — Technical Reference & Design Guide

---

# 1. Overview

This document defines the complete relational schema for the Family Tree backend system.

The system is built using:

* Python
* SQLAlchemy ORM
* Relational database (PostgreSQL recommended)
* UUID primary keys
* Foreign key constraints
* Indexed lookup fields

This schema supports:

* Authentication
* Role-based authorization
* Multi-tenant family trees
* Hierarchical person relationships

---

# 2. Design Principles

The schema follows:

* Normalized relational design
* Explicit foreign keys
* UUID primary keys
* Indexing for performance
* Clear ownership boundaries
* Extensibility for future features

---

# 3. Entity Overview

Core tables:

1. users
2. family_trees
3. persons

Planned tables:

4. marriages
5. refresh_tokens
6. audit_logs

---

# 4. users Table

Represents authenticated system users.

---

## 4.1 Fields

| Column        | Type      | Constraints      | Description            |
| ------------- | --------- | ---------------- | ---------------------- |
| id            | UUID      | PK               | Unique user identifier |
| email         | VARCHAR   | UNIQUE, NOT NULL | Login identifier       |
| password_hash | VARCHAR   | NOT NULL         | Bcrypt hashed password |
| role          | VARCHAR   | NOT NULL         | Authorization role     |
| is_active     | BOOLEAN   | DEFAULT TRUE     | Soft delete flag       |
| created_at    | TIMESTAMP | NOT NULL         | Creation timestamp     |
| updated_at    | TIMESTAMP | NOT NULL         | Last update timestamp  |

---

## 4.2 Indexes

* Unique index on `email`
* Index on `role`

---

## 4.3 Relationships

* One user → Many family_trees

---

# 5. family_trees Table

Logical container for hierarchical family data.

---

## 5.1 Fields

| Column     | Type      | Constraints    | Description            |
| ---------- | --------- | -------------- | ---------------------- |
| id         | UUID      | PK             | Unique tree identifier |
| name       | VARCHAR   | NOT NULL       | Tree name              |
| owner_id   | UUID      | FK → users.id | Tree owner             |
| is_active  | BOOLEAN   | DEFAULT TRUE   | Soft delete flag       |
| created_at | TIMESTAMP | NOT NULL       | Creation time          |
| updated_at | TIMESTAMP | NOT NULL       | Last update            |

---

## 5.2 Indexes

* Index on `owner_id`

---

## 5.3 Relationships

* One family_tree → Many persons
* Belongs to one user

---

# 6. persons Table

Represents individuals within a family tree.

Core hierarchical node.

---

## 6.1 Fields

| Column         | Type      | Constraints           | Description              |
| -------------- | --------- | --------------------- | ------------------------ |
| id             | UUID      | PK                    | Unique person identifier |
| first_name     | VARCHAR   | NOT NULL              | Given name               |
| last_name      | VARCHAR   | NULLABLE              | Family name              |
| gender         | VARCHAR   | NULLABLE              | M/F/Other                |
| date_of_birth  | DATE      | NULLABLE              | Birth date               |
| date_of_death  | DATE      | NULLABLE              | Death date               |
| family_tree_id | UUID      | FK → family_trees.id | Tree ownership           |
| parent_id      | UUID      | FK → persons.id      | Self-referencing parent  |
| spouse_id      | UUID      | FK → persons.id      | Optional spouse          |
| is_active      | BOOLEAN   | DEFAULT TRUE          | Soft delete              |
| created_at     | TIMESTAMP | NOT NULL              | Creation time            |
| updated_at     | TIMESTAMP | NOT NULL              | Last update              |

---

## 6.2 Indexes

* Index on `family_tree_id`
* Index on `parent_id`
* Index on `spouse_id`

---

## 6.3 Relationships

* Self-referencing parent-child (Adjacency List)
* Optional spouse link
* Belongs to family_tree

---

# 7. Hierarchical Modeling Strategy

Uses Adjacency List Pattern:

<pre class="overflow-visible! px-0!" data-start="3448" data-end="3478"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>parent_id → persons.id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This enables:

* Recursive traversal
* Efficient inserts
* Flexible structure

---

# 8. Data Integrity Constraints

---

## 8.1 Foreign Key Rules

* family_tree_id must exist
* parent_id must reference same table
* owner_id must exist in users

---

## 8.2 Application-Level Validations

* Prevent circular parent references
* Prevent self-parenting
* Prevent spouse self-reference
* Ensure parent belongs to same family_tree

---

# 9. Optional Future Tables

---

# 9.1 marriages Table (Recommended Upgrade)

Supports historical marriages.

---

## Fields

| Column      | Type | Description      |
| ----------- | ---- | ---------------- |
| id          | UUID | PK               |
| person1_id  | UUID | FK → persons.id |
| person2_id  | UUID | FK → persons.id |
| married_on  | DATE | Marriage date    |
| divorced_on | DATE | Nullable         |

---

Benefits:

* Multiple marriages
* Divorce tracking
* Historical accuracy

---

# 9.2 refresh_tokens Table

Supports token rotation.

---

## Fields

| Column     | Type      | Description    |
| ---------- | --------- | -------------- |
| id         | UUID      | PK             |
| user_id    | UUID      | FK → users.id |
| token      | TEXT      | Refresh token  |
| expires_at | TIMESTAMP | Expiration     |
| is_revoked | BOOLEAN   | Default FALSE  |
| created_at | TIMESTAMP | Created time   |

---

# 9.3 audit_logs Table

Tracks sensitive actions.

---

## Fields

| Column        | Type      | Description         |
| ------------- | --------- | ------------------- |
| id            | UUID      | PK                  |
| user_id       | UUID      | FK → users.id      |
| action        | VARCHAR   | Operation performed |
| resource_type | VARCHAR   | e.g. person         |
| resource_id   | UUID      | ID affected         |
| created_at    | TIMESTAMP | Timestamp           |

---

# 10. Deletion Strategy

Soft deletion recommended.

Add:

<pre class="overflow-visible! px-0!" data-start="5121" data-end="5159"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>is_active BOOLEAN DEFAULT TRUE</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Instead of physical deletion.

Benefits:

* Data recovery
* Audit safety
* Referential stability

---

# 11. Transaction Design

Use transactions for:

* Adding parent + child
* Tree restructuring
* Marriage updates
* Bulk imports

Ensure atomic operations.

---

# 12. Performance Considerations

---

## 12.1 Expected Workload

* Read-heavy queries (tree display)
* Moderate writes (adding persons)
* Rare deletes

---

## 12.2 Optimization Strategies

* Index foreign keys
* Limit recursive depth
* Use CTE for ancestry queries
* Cache tree results if needed

---

# 13. Example SQL DDL (Conceptual)

---

## users

<pre class="overflow-visible! px-0!" data-start="5780" data-end="6039"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>CREATE TABLE users (</span><br/><span>    id UUID PRIMARY KEY,</span><br/><span>    email VARCHAR UNIQUE NOT NULL,</span><br/><span>    password_hash VARCHAR NOT NULL,</span><br/><span>    role VARCHAR NOT NULL,</span><br/><span>    is_active BOOLEAN DEFAULT TRUE,</span><br/><span>    created_at TIMESTAMP NOT NULL,</span><br/><span>    updated_at TIMESTAMP NOT NULL</span><br/><span>);</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## family_trees

<pre class="overflow-visible! px-0!" data-start="6063" data-end="6298"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>CREATE TABLE family_trees (</span><br/><span>    id UUID PRIMARY KEY,</span><br/><span>    name VARCHAR NOT NULL,</span><br/><span>    owner_id UUID REFERENCES users(id),</span><br/><span>    is_active BOOLEAN DEFAULT TRUE,</span><br/><span>    created_at TIMESTAMP NOT NULL,</span><br/><span>    updated_at TIMESTAMP NOT NULL</span><br/><span>);</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## persons

<pre class="overflow-visible! px-0!" data-start="6317" data-end="6743"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>CREATE TABLE persons (</span><br/><span>    id UUID PRIMARY KEY,</span><br/><span>    first_name VARCHAR NOT NULL,</span><br/><span>    last_name VARCHAR,</span><br/><span>    gender VARCHAR,</span><br/><span>    date_of_birth DATE,</span><br/><span>    date_of_death DATE,</span><br/><span>    family_tree_id UUID REFERENCES family_trees(id),</span><br/><span>    parent_id UUID REFERENCES persons(id),</span><br/><span>    spouse_id UUID REFERENCES persons(id),</span><br/><span>    is_active BOOLEAN DEFAULT TRUE,</span><br/><span>    created_at TIMESTAMP NOT NULL,</span><br/><span>    updated_at TIMESTAMP NOT NULL</span><br/><span>);</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 14. Multi-Tenancy Enforcement

Every query must filter by:

<pre class="overflow-visible! px-0!" data-start="6812" data-end="6859"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>family_tree.owner_id == current_user.id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Or:

<pre class="overflow-visible! px-0!" data-start="6866" data-end="6908"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>family_tree_id IN user_owned_trees</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Prevents cross-tenant data leakage.

---

# 15. Migration Strategy

Use Alembic for:

* Schema versioning
* Adding new columns
* Introducing marriage table
* Adding refresh tokens

Never modify schema manually in production.

---

# 16. Schema Versioning Plan

Version 1:

* users
* family_trees
* persons

Version 2:

* marriages
* refresh_tokens

Version 3:

* audit_logs
* permissions system

---

# 17. Security Considerations

* Enforce FK constraints
* Avoid cascading deletes without review
* Validate ownership at service layer
* Never expose internal IDs without auth

---

# 18. Current Schema Maturity

| Component      | Status       |
| -------------- | ------------ |
| users          | Implemented  |
| family_trees   | Designed     |
| persons        | Core defined |
| marriages      | Planned      |
| refresh_tokens | Planned      |
| audit_logs     | Planned      |

---

# 19. Final Summary

The database schema:

* Is normalized
* Supports hierarchical modeling
* Is multi-tenant aware
* Supports RBAC integration
* Is scalable for medium-sized genealogical datasets
* Is ready for Alembic migration management

It provides a solid relational foundation for the Family Tree system.
