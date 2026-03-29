# RBAC Mini Project

A CLI-based Role-Based Access Control (RBAC) system built in Python.

## Features

- Create users and roles
- Assign roles to users
- Remove roles from users
- Add permissions to roles
- Remove permissions from roles
- Add deny permissions to roles
- Role inheritance
- Deny overrides allow
- Permission checking
- Show role hierarchy
- Explain why a user has or does not have a permission
- View audit logs
- JSON-based persistence
- Permission caching
- Unit testing with pytest
- Safe input validation for numeric command arguments

## Project Structure

```bash
rbac_project/
│
├── models/
│   ├── role.py
│   └── user.py
│
├── services/
│   └── user_service.py
│
├── storage/
│   ├── json_storage.py
│   ├── role_store.py
│   └── user_store.py
│
├── utils/
│   └── logger.py
│
├── data/
│   ├── roles.json
│   ├── users.json
│   └── audit.log
│
├── tests/
│   └── test_permissions.py
│
└── main.py