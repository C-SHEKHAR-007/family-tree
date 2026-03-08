## Authentication & Authorization Flow — Technical Reference

---

# 1. Overview

This document describes the complete authentication and authorization flow implemented in the Family Tree backend system.

The authentication system is built using:

* **FastAPI**
* SQLAlchemy ORM
* Passlib (bcrypt)
* JWT (HS256)
* Environment-based configuration
* OAuth2 compatible login flow

This system is stateless and designed for scalability.

---

# 2. Authentication Architecture

## 2.1 Core Components

| Component        | Responsibility                  |
| ---------------- | ------------------------------- |
| `security.py`  | Password hashing + JWT creation |
| `auth.py`      | Login route                     |
| `user_repo.py` | Database user lookup            |
| `.env`         | Secret configuration            |
| `config.py`    | Environment loader              |

---

# 3. Full Authentication Flow

---

## 3.1 Step 1 — User Login Request

Client sends:

<pre class="overflow-visible! px-0!" data-start="1016" data-end="1088"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>POST /auth/login</span><br/><span>Content-Type: application/x-www-form-urlencoded</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Body:

<pre class="overflow-visible! px-0!" data-start="1097" data-end="1150"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>username=admin@example.com</span><br/><span>password=Admin@123</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Note:

* `username` is used instead of `email` because OAuth2PasswordRequestForm requires it.
* Internally, username = email.

---

## 3.2 Step 2 — Credential Validation

Flow:

<pre class="overflow-visible! px-0!" data-start="1329" data-end="1391"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>auth route</span><br/><span> → get_user_by_email()</span><br/><span> → verify_password()</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Database Check

<pre class="overflow-visible! px-0!" data-start="1413" data-end="1475"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">user</span><span></span><span class="ͼn">=</span><span></span><span class="ͼt">get_user_by_email</span><span>(</span><span class="ͼt">db</span><span>, </span><span class="ͼt">form_data</span><span class="ͼn">.</span><span>username)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If user does not exist:

* Return 401 Unauthorized

### Password Verification

<pre class="overflow-visible! px-0!" data-start="1555" data-end="1620"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">verify_password</span><span>(</span><span class="ͼt">plain_password</span><span>, </span><span class="ͼt">user</span><span class="ͼn">.</span><span>password_hash)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If password invalid:

* Return 401 Unauthorized

---

## 3.3 Step 3 — JWT Creation

If credentials are valid:

<pre class="overflow-visible! px-0!" data-start="1732" data-end="1842"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">create_access_token</span><span>({</span><br/><span></span><span class="ͼr">"sub"</span><span>: </span><span class="ͼt">str</span><span>(</span><span class="ͼt">user</span><span class="ͼn">.</span><span>id),</span><br/><span></span><span class="ͼr">"email"</span><span>: </span><span class="ͼt">user</span><span class="ͼn">.</span><span>email,</span><br/><span></span><span class="ͼr">"role"</span><span>: </span><span class="ͼt">user</span><span class="ͼn">.</span><span>role</span><br/><span>})</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### JWT Payload Structure

<pre class="overflow-visible! px-0!" data-start="1871" data-end="1979"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "sub": </span><span class="ͼr">"uuid-user-id"</span><span>,</span><br/><span>  "email": </span><span class="ͼr">"user@email.com"</span><span>,</span><br/><span>  "role": </span><span class="ͼr">"admin"</span><span>,</span><br/><span>  "exp": </span><span class="ͼq">1700000000</span><br/><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Important Fields

| Field | Purpose              |
| ----- | -------------------- |
| sub   | User identifier      |
| email | Identity reference   |
| role  | Authorization checks |
| exp   | Expiration time      |

---

## 3.4 Step 4 — Token Returned

Response:

<pre class="overflow-visible! px-0!" data-start="2208" data-end="2309"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "access_token": </span><span class="ͼr">"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."</span><span>,</span><br/><span>  "token_type": </span><span class="ͼr">"bearer"</span><br/><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Client must store token securely.

---

# 4. Protected Route Flow

When accessing protected endpoints:

<pre class="overflow-visible! px-0!" data-start="2415" data-end="2452"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Authorization: Bearer <token></span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## 4.1 Token Extraction

FastAPI dependency:

<pre class="overflow-visible! px-0!" data-start="2505" data-end="2573"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Token extracted from header.

---

## 4.2 Token Decoding

Inside `get_current_user()`:

<pre class="overflow-visible! px-0!" data-start="2663" data-end="2740"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">payload</span><span></span><span class="ͼn">=</span><span></span><span class="ͼt">jwt</span><span class="ͼn">.</span><span>decode(</span><span class="ͼt">token</span><span>, </span><span class="ͼt">SECRET_KEY</span><span>, </span><span class="ͼt">algorithms</span><span class="ͼn">=</span><span>[</span><span class="ͼt">ALGORITHM</span><span>])</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If:

* Token invalid → 401
* Token expired → 401
* Signature invalid → 401

---

## 4.3 User Reconstruction

From payload:

<pre class="overflow-visible! px-0!" data-start="2865" data-end="2907"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">user_id</span><span></span><span class="ͼn">=</span><span></span><span class="ͼt">payload</span><span class="ͼn">.</span><span>get(</span><span class="ͼr">"sub"</span><span>)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Fetch user from database:

<pre class="overflow-visible! px-0!" data-start="2936" data-end="2999"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼt">db</span><span class="ͼn">.</span><span>query(</span><span class="ͼt">User</span><span>)</span><span class="ͼn">.</span><span>filter(</span><span class="ͼt">User</span><span class="ͼn">.</span><span>id </span><span class="ͼn">==</span><span></span><span class="ͼt">user_id</span><span>)</span><span class="ͼn">.</span><span>first()</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If user does not exist:

* Return 401

---

# 5. Role-Based Authorization (RBAC)

## 5.1 Role Stored In

* Database
* JWT payload

Example roles:

<pre class="overflow-visible! px-0!" data-start="3147" data-end="3174"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>admin</span><br/><span>member</span><br/><span>viewer</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## 5.2 Admin-Only Route Example

Future implementation:

<pre class="overflow-visible! px-0!" data-start="3238" data-end="3425"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼn">def</span><span></span><span class="ͼt">admin_required</span><span>(</span><span class="ͼt">current_user</span><span>: </span><span class="ͼt">User</span><span></span><span class="ͼn">=</span><span></span><span class="ͼt">Depends</span><span>(</span><span class="ͼt">get_current_user</span><span>)):</span><br/><span></span><span class="ͼn">if</span><span></span><span class="ͼt">current_user</span><span class="ͼn">.</span><span>role </span><span class="ͼn">!=</span><span></span><span class="ͼr">"admin"</span><span>:</span><br/><span></span><span class="ͼn">raise</span><span></span><span class="ͼt">HTTPException</span><span>(</span><span class="ͼt">status_code</span><span class="ͼn">=</span><span class="ͼq">403</span><span>, </span><span class="ͼt">detail</span><span class="ͼn">=</span><span class="ͼr">"Access denied"</span><span>)</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Used as:

<pre class="overflow-visible! px-0!" data-start="3437" data-end="3568"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼm">@</span><span class="ͼt">router</span><span class="ͼn">.</span><span class="ͼt">get</span><span>(</span><span class="ͼr">"/admin-only"</span><span>)</span><br/><span class="ͼn">def</span><span></span><span class="ͼt">admin_dashboard</span><span>(</span><span class="ͼt">user</span><span class="ͼn">=</span><span class="ͼt">Depends</span><span>(</span><span class="ͼt">admin_required</span><span>)):</span><br/><span></span><span class="ͼn">return</span><span> {</span><span class="ͼr">"message"</span><span>: </span><span class="ͼr">"Welcome admin"</span><span>}</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 6. Security Design Decisions

---

## 6.1 Stateless Authentication

No server-side sessions.

Advantages:

* Horizontal scaling ready
* No Redis required
* Microservice compatible

---

## 6.2 JWT Expiration

Configured in `.env`:

<pre class="overflow-visible! px-0!" data-start="3808" data-end="3846"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>ACCESS_TOKEN_EXPIRE_MINUTES=60</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Expiration included in token payload.

---

## 6.3 Password Security

* Bcrypt hashing
* Salted automatically
* Plain passwords never stored
* Verification uses secure compare

---

# 7. Error Handling Standards

| Scenario            | Status Code |
| ------------------- | ----------- |
| Invalid credentials | 401         |
| Expired token       | 401         |
| Invalid token       | 401         |
| Unauthorized role   | 403         |
| User not found      | 401         |

---

# 8. Attack Mitigation Strategy

---

## 8.1 Brute Force Protection (Planned)

Future:

* Login attempt counter
* Account lock after N attempts
* IP rate limiting

---

## 8.2 Token Security

Current:

* HS256 symmetric encryption

Future options:

* RS256 asymmetric
* Key rotation
* Token versioning

---

## 8.3 Secret Management

Secrets stored in:

<pre class="overflow-visible! px-0!" data-start="4605" data-end="4617"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>.env</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Never committed to git.

---

# 9. Future Authentication Enhancements

---

## 9.1 Refresh Token System

Planned:

* Short-lived access token (15–60 min)
* Long-lived refresh token (7 days)
* Rotation mechanism
* DB stored refresh tokens

---

## 9.2 Logout Support

Option 1:

* Token blacklist table

Option 2:

* Token versioning in user table

---

## 9.3 Password Reset Flow

Planned:

* Email-based reset token
* Time-limited reset link
* One-time use

---

## 9.4 Email Verification

Planned:

* Verification token
* Activate account after email confirm

---

# 10. Complete Authentication Lifecycle

<pre class="overflow-visible! px-0!" data-start="5225" data-end="5473"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>User registers</span><br/><span> → Password hashed</span><br/><span> → Stored in DB</span><br/><br/><span>User logs in</span><br/><span> → Password verified</span><br/><span> → JWT generated</span><br/><span> → Token returned</span><br/><br/><span>User accesses protected route</span><br/><span> → Token validated</span><br/><span> → Payload decoded</span><br/><span> → User fetched</span><br/><span> → Role validated</span><br/><span> → Access granted</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# 11. Performance Characteristics

* Login: O(1) DB lookup
* Token validation: O(1)
* Stateless
* No server memory overhead per session

---

# 12. Current Authentication Maturity

| Feature           | Status   |
| ----------------- | -------- |
| Password hashing  | Complete |
| JWT login         | Complete |
| OAuth2 compatible | Complete |
| Protected routes  | Pending  |
| RBAC              | Planned  |
| Refresh tokens    | Planned  |
| Logout            | Planned  |
| Rate limiting     | Planned  |

---

# 13. Design Philosophy

* Keep authentication centralized
* Keep authorization layered
* Keep JWT minimal but sufficient
* Never trust client-side data
* Always validate role server-side

---

# 14. Final Summary

The authentication system:

* Is secure
* Is stateless
* Is scalable
* Is production-ready for MVP
* Is structured for future RBAC & refresh token upgrades

You now have a solid authentication foundation.
