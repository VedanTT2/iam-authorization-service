# IAM Authorization Service

A Python-based authorization engine that implements Role-Based Access Control (RBAC) using a layered architecture.
This project simulates how real-world Identity and Access Management (IAM) systems evaluate permissions for users based on assigned roles and role hierarchies.
The system supports role inheritance and recursive permission resolution, similar to enterprise IAM implementations.

## Features

Role-Based Access Control (RBAC)
- Role inheritance
- Allow and deny permissions
- Permission caching
- Audit logging
- Explain permission (why access is granted/denied)
- Admin queries:
  - who_has_permission
  - who_has_role
- Full permission lifecycle:
  - add_permission
  - remove_permission

## Tech Stack
- Python
- JSON-based storage

## Key Concepts Implemented
- RBAC model
- Permission inheritance
- Deny overrides allow
- Caching for performance optimization
- Audit logging for traceability

## Sample Commands
create_user 1 vedant  
create_role 5 IT  
assign_role 1 5  
check_permission 1 read  
view_logs  

## Future Improvements
- API version (Flask/FastAPI)
- JWT authentication
- Database integration
