
# RBAC_DESIGN.md

## Role-Based Access Control — Architecture & Implementation Guide

---

# 1. Overview

This document defines the Role-Based Access Control (RBAC) strategy for the Family Tree backend system.

RBAC is used to:

* Restrict access to sensitive operations
* Enforce ownership boundaries
* Prevent cross-user data access
* Enable admin-level operations

The system integrates with:

* JWT authentication
* User model role field
* FastAPI dependency injection

---

# 2. RBAC Philosophy

The system follows:

**Stateless Role-Based Authorization**

* Role stored in database
* Role embedded inside JWT
* Role validated at request time
* No server-side session state

---

# 3. Role Definitions

Initial roles:

| Role   | Description         |
| ------ | ------------------- |
| admin  | Full system access  |
| member | Own tree management |
| viewer | Read-only access    |

Future roles may include:

* super_admin
* moderator
* tree_editor

---

# 4. Where Roles Are Stored

Roles exist in:

## 4.1 Database

User table includes:

<pre class="overflow-visible! px-0!" data-start="1131" data-end="1151"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>role: string</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Example:

<pre class="overflow-visible! px-0!" data-start="1163" data-end="1190"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>admin</span><br/><span>member</span><br/><span>viewer</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## 4.2 JWT Payload

When login succeeds, token contains:

<pre class="overflow-visible! px-0!" data-start="1255" data-end="1358"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "sub": </span><span class="ͼr">"user_id"</span><span>,</span><br/><span>  "email": </span><span class="ͼr">"user@email.com"</span><span>,</span><br/><span>  "role": </span><span class="ͼr">"admin"</span><span>,</span><br/><span>  "exp": </span><span class="ͼq">1700000000</span><br/><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This allows:

* Quick role validation
* Reduced DB queries for simple checks
* Stateless scaling

---

# 5. Authorization Flow

---

# 5.1 Protected Endpoint Flow

<pre class="overflow-visible! px-0!" data-start="1524" data-end="1668"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Request</span><br/><span> → Extract JWT</span><br/><span> → Decode token</span><br/><span> → Validate signature</span><br/><span> → Check expiration</span><br/><span> → Extract role</span><br/><span> → Validate permission</span><br/><span> → Allow or deny</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6. Implementation Strategy

---

# 6.1 Step 1 — Authentication Dependency

Create:

<pre class="overflow-visible! px-0!" data-start="1761" data-end="1787"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>get_current_user()</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Responsibilities:

* Decode JWT
* Validate token
* Fetch user from DB
* Return User object

---

# 6.2 Step 2 — Role Guard Dependency

Create:

<pre class="overflow-visible! px-0!" data-start="1933" data-end="1964"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>require_role(role: str)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Example implementation logic:

<pre class="overflow-visible! px-0!" data-start="1997" data-end="2065"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>If current_user.role != required_role</span><br/><span> → raise 403 Forbidden</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6.3 Step 3 — Usage in Routes

Example:

<pre class="overflow-visible! px-0!" data-start="2114" data-end="2210"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>@router.delete("/users/{id}")</span><br/><span>def delete_user(..., user=Depends(require_role("admin"))):</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 7. Authorization Levels

---

# 7.1 Admin Permissions

Admin can:

* Delete any user
* Modify any family tree
* View all trees
* Manage system settings

---

# 7.2 Member Permissions

Member can:

* Create family tree
* Edit own tree
* Add/remove persons
* View own data

Member cannot:

* Access other users' trees
* Delete other users

---

# 7.3 Viewer Permissions

Viewer can:

* View tree
* Search family members

Viewer cannot:

* Modify data
* Delete nodes

---

# 8. Ownership-Based Access

Role-based access alone is not enough.

We must also enforce:

<pre class="overflow-visible! px-0!" data-start="2781" data-end="2809"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Ownership validation</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Example:

Even if user is "member":

They can only modify trees where:

<pre class="overflow-visible! px-0!" data-start="2883" data-end="2930"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>family_tree.owner_id == current_user.id</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 9. Access Control Layers

Authorization happens at two levels:

---

## 9.1 Role-Level Check

"Does this role allow this type of action?"

---

## 9.2 Resource Ownership Check

"Does this user own this specific resource?"

Both must pass.

---

# 10. Permission Matrix

| Action        | Admin | Member | Viewer |
| ------------- | ----- | ------ | ------ |
| Login         | ✔    | ✔     | ✔     |
| Create Tree   | ✔    | ✔     | ✖     |
| Edit Own Tree | ✔    | ✔     | ✖     |
| Edit Any Tree | ✔    | ✖     | ✖     |
| Delete User   | ✔    | ✖     | ✖     |
| View Own Tree | ✔    | ✔     | ✔     |
| View Any Tree | ✔    | ✖     | ✖     |

---

# 11. HTTP Status Codes

| Scenario           | Status |
| ------------------ | ------ |
| Invalid token      | 401    |
| Expired token      | 401    |
| Missing token      | 401    |
| Insufficient role  | 403    |
| Not resource owner | 403    |

---

# 12. Token Trust Model

Although role is inside JWT:

We still fetch user from database during protected requests.

Why?

* Prevent access if user deleted
* Prevent access if role changed
* Enable role revocation

---

# 13. Security Considerations

---

## 13.1 Role Escalation Protection

User cannot modify their own role.

Admin-only endpoint required for role updates.

---

## 13.2 Token Forgery Protection

* SECRET_KEY stored in `.env`
* HS256 signature validation
* Token expiration enforced

---

## 13.3 Role Change Handling

If admin changes role:

Old tokens remain valid until expiration.

Future improvement:

* Token versioning
* Token revocation list

---

# 14. Future RBAC Enhancements

---

## 14.1 Permission-Based System (Advanced)

Instead of simple roles:

Create:

<pre class="overflow-visible! px-0!" data-start="4483" data-end="4543"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>permissions table</span><br/><span>roles table</span><br/><span>role_permissions table</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This enables fine-grained control:

Example:

* tree:read
* tree:write
* user:delete

---

## 14.2 Multi-Role Support

Allow:

<pre class="overflow-visible! px-0!" data-start="4672" data-end="4696"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>roles: List[str]</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Instead of single role.

---

## 14.3 Dynamic Policy Engine

Future enterprise version:

Attribute-Based Access Control (ABAC).

Based on:

* Role
* Ownership
* Time
* Relationship depth

---

# 15. Scalability Design

RBAC is stateless.

Scaling horizontally:

* No shared session store needed
* JWT validated independently
* Role embedded in token

---

# 16. Testing Strategy

---

## 16.1 Unit Tests

* Token decoding
* Role guard logic
* Ownership validation

---

## 16.2 Integration Tests

* Login → access protected route
* Member trying admin route
* Viewer trying modify route

---

# 17. Common Mistakes to Avoid

* Checking role in route manually instead of dependency
* Trusting JWT role without DB validation
* Forgetting ownership check
* Allowing role modification via user update endpoint

---

# 18. Example Authorization Lifecycle

<pre class="overflow-visible! px-0!" data-start="5549" data-end="5705"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>User logs in</span><br/><span> → Token issued</span><br/><br/><span>User accesses /tree/123/delete</span><br/><span> → Token decoded</span><br/><span> → Role checked</span><br/><span> → Tree owner validated</span><br/><span> → Operation allowed or denied</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 19. Current Status

| Feature                 | Status   |
| ----------------------- | -------- |
| Role field in User      | Complete |
| Role inside JWT         | Complete |
| get_current_user        | Planned  |
| require_role dependency | Planned  |
| Ownership validation    | Planned  |
| Admin-only routes       | Planned  |

---

# 20. Final Summary

The RBAC system:

* Uses role-based authorization
* Is stateless
* Supports ownership checks
* Is scalable
* Is designed for future expansion

It provides:

* Secure route guarding
* Clear permission boundaries
* Clean dependency-based enforcement
* Future extensibility for enterprise-level access control
