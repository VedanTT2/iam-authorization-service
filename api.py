from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from models.user import User
from models.role import Role
from storage.role_store import RoleStore
from storage.user_store import UserStore
from services.user_service import UserService

app = FastAPI(title="RBAC Authorization Service")

# initialize stores and service
role_store = RoleStore()
user_store = UserStore()
user_service = UserService(role_store)

# JWT settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
def home():
    return {"message": "RBAC API is running"}


@app.post("/login")
def login(username: str):
    token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@app.post("/users")
def create_user(user_id: int, username: str):
    user = User(user_id, username)

    if not user_store.add_user(user):
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": f"User '{username}' created successfully"}


@app.post("/roles")
def create_role(role_id: int, role_name: str):
    role = Role(role_id, role_name)

    if not role_store.add_role(role):
        raise HTTPException(status_code=400, detail="Role already exists")

    return {"message": f"Role '{role_name}' created successfully"}


@app.post("/assign-role")
def assign_role(user_id: int, role_id: int, current_user=Depends(get_current_user)):
    user = user_store.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user_service.assign_role_to_user(user, role_id)
        user_store.save_users()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Role {role_id} assigned to user {user.username}"}


@app.get("/check-permission")
def check_permission(user_id: int, permission: str, current_user=Depends(get_current_user)):
    user_obj = user_store.get_user(user_id)

    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    result = user_service.user_has_permission(user_obj, permission)

    return {
        "user": user_obj.username,
        "permission": permission,
        "has_permission": result
    }


@app.post("/roles/{role_id}/permissions")
def add_permission(role_id: int, permission: str, current_user=Depends(get_current_user)):
    try:
        role = role_store.add_permission_to_role(role_id, permission)
        user_service.invalidate_all_caches()
        return {"message": f"Permission '{permission}' added to role '{role.name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/roles/{role_id}/deny")
def deny_permission(role_id: int, permission: str, current_user=Depends(get_current_user)):
    try:
        role = role_store.add_deny_permission_to_role(role_id, permission)
        user_service.invalidate_all_caches()
        return {"message": f"Permission '{permission}' denied for role '{role.name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/roles/{role_id}/permissions")
def remove_permission(role_id: int, permission: str, current_user=Depends(get_current_user)):
    try:
        role = role_store.remove_permission_from_role(role_id, permission)

        if role is None:
            raise HTTPException(status_code=404, detail="Permission not found")

        user_service.invalidate_all_caches()
        return {"message": f"Permission '{permission}' removed from role '{role.name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/remove-role")
def remove_role(user_id: int, role_id: int, current_user=Depends(get_current_user)):
    user = user_store.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        removed = user_service.remove_role_from_user(user, role_id)

        if not removed:
            raise HTTPException(status_code=400, detail="User does not have this role")

        user_store.save_users()
        return {"message": f"Role {role_id} removed from user {user.username}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}")
def describe_user(user_id: int, current_user=Depends(get_current_user)):
    user = user_store.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    permissions = user_service.get_user_permissions(user)

    return {
        "user_id": user.user_id,
        "username": user.username,
        "roles": list(user.role_ids),
        "allowed_permissions": list(permissions["allowed"]),
        "denied_permissions": list(permissions["denied"])
    }