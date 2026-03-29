# RBAC System

A Role-Based Access Control (RBAC) engine built in Python — designed to demonstrate core IAM concepts including role inheritance, explicit deny semantics, permission caching, and audit logging.

Built as a portfolio project for transitioning into IAM / Security Engineering roles at product-based companies.

---

## What is RBAC?

Role-Based Access Control is the foundation of most enterprise IAM systems. Instead of assigning permissions directly to users, permissions are assigned to **roles**, and roles are assigned to users. This makes access management scalable and auditable.

This project implements a production-inspired RBAC model with:

- **Role inheritance** — roles can inherit permissions from parent roles, forming a hierarchy
- **Explicit deny semantics** — a denied permission always overrides an allowed one, even across inheritance chains (same model used by AWS IAM and Azure RBAC)
- **Permission caching** — effective permissions are computed once and cached per user, with targeted invalidation on role changes
- **Audit logging** — every access decision and mutation is written to a structured log file
- **Cycle detection** — the system prevents circular inheritance chains at assignment time

---

## Project Structure

```
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
└── main.py               # CLI entry point
```

---

## Setup & Installation

**Requirements:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/your-username/rbac-project.git
cd rbac-project

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest
```

No external dependencies required for the core system.

---

## Running the CLI

```bash
python main.py
```

You will see a list of available commands and an interactive prompt.

---

## Available Commands

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

```
# Create roles
create_role 1 Viewer
create_role 2 Editor
create_role 3 Admin

# Set up inheritance: Editor inherits from Viewer
add_parent 2 1

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

**Deny always wins.** If a user has a role that allows a permission and another role (or an inherited role) that denies it, the deny wins. This matches the principle of least privilege used in enterprise IAM systems.

**Inheritance is a DAG, not a tree.** A role can have multiple parent roles. The system walks the full inheritance graph when computing effective permissions, with cycle detection to prevent infinite loops.

**Cache invalidation is scoped.** When a user's role changes, only that user's cache is cleared. When a role's permissions change (affecting potentially all users), the entire cache is cleared. This avoids stale permission decisions without recomputing everything unnecessarily.

**Storage is pluggable.** The store layer (`role_store.py`, `user_store.py`) abstracts all persistence behind a clean interface. Swapping JSON for a database only requires changes in the store layer — the service and model layers are unaffected.

---

## Running Tests

```bash
pytest tests/test_permissions.py -v
```

Test coverage includes:

- Deny overrides allow (direct and inherited)
- Multi-role conflict resolution
- Deep inheritance chains (3+ levels)
- Permission cache population and hit verification
- Cache invalidation on role removal
- User with no roles has no permissions
- Cycle detection raises `ValueError`

---

## Roadmap

- [ ] **FastAPI REST layer** — expose all operations as HTTP endpoints (`POST /users`, `GET /users/{id}/permissions`, etc.)
- [ ] **Authentication** — API key or JWT-based auth to protect the API itself
- [ ] **Database backend** — replace JSON storage with SQLite or PostgreSQL
- [ ] **Wildcard permissions** — support `*` to mean all permissions (AWS IAM style)
- [ ] **Role deletion cleanup** — automatically unassign deleted roles from all users

---

## Why I Built This

I'm a SAP Security consultant transitioning into IAM / Security Engineering at a product-based company. I built this project to demonstrate hands-on understanding of RBAC concepts beyond configuration — including the engine design, deny semantics, inheritance graphs, and the kind of service-layer thinking that underpins real IAM systems.