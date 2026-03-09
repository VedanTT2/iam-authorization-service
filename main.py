from models.user import User
from models.role import Role
from storage.role_store import RoleStore
from services.user_service import UserService

role_store = RoleStore()  # Initialize role store
user_service = UserService(role_store)

# create roles
admin = Role(1, "Admin")
admin.add_permission("Read")
admin.add_permission("Write")
admin.add_permission("Delete")
admin.add_permission("Create")

associate = Role(2, "associate")
associate.add_permission("Find")


# Store roles in RoleStore
role_store.add_role(admin)
role_store.add_role(associate)

# User creation
u1 = User(89,"Vedant")
u2 = User(80,"Vedant ka boss")

# assign role to user
user_service.assign_role_to_user(u1, 1)
user_service.assign_role_to_user(u1, 2)

# test permissions
print("User has write", user_service.user_has_permission(u1,"write"))
print("User has find", user_service.user_has_permission(u1,"Find"))
User.remove_role(u1,1)

print("User has write", user_service.user_has_permission(u1,"write"))



