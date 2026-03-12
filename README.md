# IAM Authorization Service

A Python-based authorization engine that implements Role-Based Access Control (RBAC) using a layered architecture.  
This project is being built step by step to simulate how real-world IAM and access control systems evaluate permissions for users based on assigned roles.

## Current Features

- Role model with permission management
- User model supporting multiple role assignments
- Role inheritance (hierarchical RBAC)
- Recursive permission resolution across inherited roles
- Service layer for authorization logic
- JSON-based persistence layer
- Case-insensitive permission handling
- Modular architecture (models / services / storage)

