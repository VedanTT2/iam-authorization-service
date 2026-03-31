# RBAC System

A Role-Based Access Control (RBAC) authorization engine built in Python, designed to demonstrate core IAM concepts including role inheritance, explicit deny semantics, permission caching, audit logging, and JWT-protected APIs.

Built as a portfolio project for transitioning into IAM / Security Engineering roles at product-based companies.

---

## What is RBAC?

Role-Based Access Control is the foundation of most enterprise IAM systems. Instead of assigning permissions directly to users, permissions are assigned to **roles**, and roles are assigned to users. This makes access management scalable and auditable.

This project implements a production-inspired RBAC model with:

- **Role inheritance** — roles can inherit permissions from parent roles, forming a hierarchy
- **Explicit deny semantics** — a denied permission always overrides an allowed one, even across inheritance chains
- **Permission caching** — effective permissions are computed once and cached per user, with targeted invalidation on role changes
- **Audit logging** — every access decision and mutation is written to a structured log file
- **Cycle detection** — the system prevents circular inheritance chains at assignment time
- **FastAPI support** — the same RBAC engine is exposed through REST APIs
- **JWT-based protection** — protected endpoints require bearer token authentication

---

## Project Structure

```text
rbac_project/
│
├── models/
│   ├── role.py           # Role entity: permissions, deny rules, parent roles
│   └── user.py           # User entity: identity and assigned role IDs
│
├── services/
│   └── user_service.py   # Business logic: permission checks, caching, role assignment
│
├── storage/
│   ├── json_storage.py   # JSON read/write helpers
│   ├── role_store.py     # Role persistence and mutation operations
│   └── user_store.py     # User persistence and mutation operations
│
├── utils/
│   └── logger.py         # Structured audit logger
│
├── data/
│   ├── roles.json        # Persisted roles
│   ├── users.json        # Persisted users
│   └── audit.log         # Audit trail
│
├── tests/
│   └── test_permissions.py  # pytest unit tests
│
├── main.py               # CLI entry point
└── api.py                # FastAPI entry point
```

---

## Architecture Overview

The system follows a layered architecture:

- **Models** — represent core entities (`User`, `Role`)
- **Stores** — handle persistence (currently JSON-based)
- **Service Layer** — contains business logic such as permission evaluation, caching, and role assignment
- **CLI Layer** — handles interactive command-line operations
- **API Layer** — exposes the same logic through FastAPI endpoints

This separation improves:

- maintainability
- testability
- reuse across CLI and API
- easy extension later, such as replacing JSON with a database

---

## Setup & Installation

**Requirements:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/VedantTT2/iam-authorization-service.git
cd iam-authorization-service

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest fastapi uvicorn python-jose
```

---

## Running the CLI

```bash
python main.py
```

You will see a list of available commands and an interactive prompt.

---

## Running the API (FastAPI)

This project also exposes a REST API using FastAPI.

### Start the server

```bash
uvicorn api:app --reload
```

### Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

### Authentication Flow

1. Call `/login` with a username
2. Copy the returned `access_token`
3. Click **Authorize** in Swagger
4. Paste the token
5. Call protected endpoints

### Example Endpoints

- `POST /users` — create user
- `POST /roles` — create role
- `POST /assign-role` — assign role to user
- `GET /check-permission` — check whether a user has a permission
- `GET /users/{user_id}` — return a user's roles and effective permissions
- `POST /roles/{role_id}/permissions` — add permission to role
- `POST /roles/{role_id}/deny` — explicitly deny permission on role
- `DELETE /roles/{role_id}/permissions` — remove permission from role

---

## Available CLI Commands

| Command | Description |
|---|---|
| `create_user <user_id> <username>` | Create a new user |
| `create_role <role_id> <role_name>` | Create a new role |
| `assign_role <user_id> <role_id>` | Assign a role to a user |
| `remove_role <user_id> <role_id>` | Remove a role from a user |
| `add_permission <role_id> <permission>` | Grant a permission to a role |
| `deny_permission <role_id> <permission>` | Explicitly deny a permission on a role |
| `remove_permission <role_id> <permission>` | Remove a granted permission from a role |
| `add_parent <child_role_id> <parent_role_id>` | Set up role inheritance |
| `check_permission <user_id> <permission>` | Check if a user has a permission |
| `describe_user <user_id>` | Show a user's roles and effective permissions |
| `why_user_has_permission <user_id> <permission>` | Trace the allow/deny decision path |
| `explain_permission <user_id> <permission>` | Detailed explanation with full inheritance path |
| `who_has_permission <permission>` | List all users who have a given permission |
| `who_has_role <role_id>` | List all users assigned a given role |
| `list_users` | List all users |
| `list_roles` | List all roles with permissions and parents |
| `show_roles` | Display role hierarchy |
| `view_logs` | Show last 10 audit log entries |
| `exit` | Exit the CLI |

---

## Example Usage

```text
# Create roles
create_role 1 Viewer
create_role 2 Editor
create_role 3 Admin

# Set up inheritance: Editor inherits from Viewer
add_parent 2 1
add_parent 3 2

# Grant and deny permissions
add_permission 1 read
add_permission 2 write
deny_permission 3 write

# Create a user and assign roles
create_user 1 vedant
assign_role 1 3

# Check permissions
check_permission 1 read
> User 'vedant' HAS 'read' permission.

check_permission 1 write
> User 'vedant' DOES NOT HAVE 'write' permission.

# Trace why
explain_permission 1 write
> FINAL RESULT: DENIED
> WHY: Admin -> DENY:write
> ALSO FOUND ALLOW PATH: Admin -> Editor -> write
> NOTE: DENY overrides ALLOW.
```

---

## Key Design Decisions

**Deny always wins.** If a user has a role that allows a permission and another role, direct or inherited, that denies it, the deny wins. This follows the principle of least privilege.

**Inheritance is modeled as a DAG, not a tree.** A role can have multiple parent roles. The system walks the full inheritance graph when computing effective permissions, while preventing cycles at assignment time.

**Cache invalidation is scoped.** When a user's role assignments change, only that user's cache is cleared. When a role's permissions change, all cached permission sets are invalidated.

**Storage is pluggable.** The store layer (`role_store.py`, `user_store.py`) abstracts persistence behind a clean interface. Replacing JSON with a database should mainly affect the storage layer.

**Performance considerations.** Permission checks are optimized using a per-user cache. After the first computation, subsequent permission checks avoid repeated inheritance traversal and become fast dictionary lookups.

---

## Running Tests

```bash
python -m pytest
```

Test coverage includes:

- deny overrides allow
- multi-role conflict resolution
- inheritance chains
- permission cache population
- cache invalidation on role removal
- user with no roles has no permissions
- cycle detection raises `ValueError`

---

## Security Considerations

- JWT authentication is implemented using a shared secret key
- Current login is a mock implementation and does not verify passwords
- The secret key is currently hardcoded for learning/demo purposes

In a production system:

- secrets should be loaded from environment variables or a secrets manager
- passwords should be hashed using a secure algorithm such as bcrypt
- JWTs should include expiry claims such as `exp`
- sensitive endpoints should enforce stronger role-based API authorization, such as admin-only access

---

## Roadmap

- [x] RBAC engine with inheritance and deny override
- [x] Permission caching
- [x] CLI interface
- [x] Unit testing with pytest
- [x] FastAPI REST API
- [x] Basic JWT authentication
- [ ] Refresh token implementation
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Role-based API authorization (admin-only routes)
- [ ] Dockerization
- [ ] Role deletion cleanup

---

## Why I Built This

I'm a SAP Security consultant transitioning into IAM / Security Engineering at a product-based company. I built this project to demonstrate hands-on understanding of RBAC concepts beyond configuration, including authorization engine design, explicit deny semantics, inheritance graphs, caching, testing, and backend API integration.
