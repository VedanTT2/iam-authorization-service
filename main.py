from models.user import User
from models.role import Role
from storage.role_store import RoleStore
from services.user_service import UserService

role_store = RoleStore()  # Initialize role store

viewer = Role(1, "Viewer")
viewer.add_permission("read")

editor = Role(2, "Editor")
editor.add_permission("write")

admin = Role(3, "Admin")
admin.add_parent_role(1)
admin.add_parent_role(2)

role_store.add_role(viewer)
role_store.add_role(editor)
role_store.add_role(admin)

print("admin parents", admin.parent_roles)
print("admin from store parents:", role_store.get_role(3).parent_roles)
print(admin.get_all_permissions(role_store))
print(admin.has_permission("read", role_store))
print(admin.has_permission("write", role_store))
print(admin.has_permission("delete", role_store))



