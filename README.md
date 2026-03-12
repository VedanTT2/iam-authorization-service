# IAM Authorization Service

A Python-based authorization engine that implements Role-Based Access Control (RBAC) using a layered architecture.
This project simulates how real-world Identity and Access Management (IAM) systems evaluate permissions for users based on assigned roles and role hierarchies.
The system supports role inheritance and recursive permission resolution, similar to enterprise IAM implementations.

## Current Features

- Role model with permission management
- User model supporting multiple role assignments
- Role inheritance (hierarchical RBAC)
- Recursive permission resolution across inherited roles
- Service layer for authorization logic
- JSON-based persistence layer
- Case-insensitive permission handling
- Modular architecture (models / services / storage)

