# IAM Authorization Service

A Python-based authorization engine that implements Role-Based Access Control (RBAC) using a layered architecture.
This project simulates how real-world Identity and Access Management (IAM) systems evaluate permissions for users based on assigned roles and role hierarchies.
The system supports role inheritance and recursive permission resolution, similar to enterprise IAM implementations.

## Features

- User creation and storage
- Role creation and storage
- Assign roles to users
- Permission checking
- Hierarchical role inheritance
- Recursive permission resolution using DFS
- Cycle-safe traversal using a visited set
- Cycle prevention while assigning parent roles
- Describe user access with effective permissions
- Visualize role hierarchy
- Trace why a user has a permission
- Persistent storage using JSON files
- CLI-based interaction
- Permission caching for fast authorization
- Permission explanation engine
- Role hierarchy graph visualisation
- Access audit: who_has_permission
- Explicit deny permissions (DENY overrides ALLOW)
