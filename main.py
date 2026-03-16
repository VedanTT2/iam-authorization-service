# Import User model (represents identity object)
from models.user import User

# Import stores responsible for loading/saving data from JSON
from storage.role_store import RoleStore
from storage.user_store import UserStore

# Import service layer that contains business logic
# (role assignment and permission checking)
from services.user_service import UserService


# Initialize stores
# RoleStore loads roles from roles.json
role_store = RoleStore()

# UserStore loads users from users.json
user_store = UserStore()

# UserService uses RoleStore to perform permission checks
user_service = UserService(role_store)


# CLI introduction
print("RBAC CLI Started")

# List of commands user can run
print("Commands:")
print("create_user <user_id> <username>")
print("list_users")
print("list_roles")
print("assign_role <user_id> <role_id>")
print("check_permission <user_id> <permission>")
print("exit")


# Infinite loop so CLI keeps running until user types exit
while True:

    # Read user command
    command = input("\nEnter command: ").strip()

    # Ignore empty input
    if not command:
        continue

    # Split command into parts
    # Example: "create_user 1 vedant"
    # parts = ["create_user", "1", "vedant"]
    parts = command.split()

    # First word is the action/command
    action = parts[0].lower()


    # Exit program
    if action == "exit":
        print("Exiting RBAC CLI.")
        break


    # CREATE USER
    elif action == "create_user":

        # Command must contain exactly 3 parts
        if len(parts) != 3:
            print("Usage: create_user <user_id> <username>")
            continue

        user_id = int(parts[1])
        username = parts[2]

        # Create user object
        user = User(user_id, username)

        # Store user in UserStore
        if user_store.add_user(user):
            print(f"User '{username}' created successfully.")
        else:
            print("User ID already exists.")


    # LIST USERS
    elif action == "list_users":

        # Fetch all users from storage
        users = user_store.get_all_users()

        if not users:
            print("No users found.")
        else:
            print("Users:")

            # Display each user
            for user in users:
                print(
                    f"ID: {user.user_id}, "
                    f"Username: {user.username}, "
                    f"Roles: {list(user.role_ids)}"
                )


    # LIST ROLES
    elif action == "list_roles":

        # Fetch roles from RoleStore
        roles = role_store.get_all_roles()

        if not roles:
            print("No roles found.")
        else:
            print("Roles:")

            for role in roles:
                print(
                    f"ID: {role.role_id}, "
                    f"Name: {role.name}, "
                    f"Permissions: {list(role.permissions)}, "
                    f"Parents: {list(role.parent_roles)}"
                )


    # ASSIGN ROLE TO USER
    elif action == "assign_role":

        if len(parts) != 3:
            print("Usage: assign_role <user_id> <role_id>")
            continue

        user_id = int(parts[1])
        role_id = int(parts[2])

        # Retrieve user from storage
        user = user_store.get_user(user_id)

        if not user:
            print("User not found.")
            continue

        try:
            # Use service layer to assign role
            user_service.assign_role_to_user(user, role_id)

            # Save changes to JSON
            user_store._save_users()

            print(f"Role {role_id} assigned to user {user.username}.")

        except ValueError as e:
            print(e)


    # CHECK USER PERMISSION
    elif action == "check_permission":

        if len(parts) != 3:
            print("Usage: check_permission <user_id> <permission>")
            continue

        user_id = int(parts[1])
        permission = parts[2]

        # Retrieve user
        user = user_store.get_user(user_id)

        if not user:
            print("User not found.")
            continue

        # Check permission using service layer
        if user_service.user_has_permission(user, permission):
            print(f"User '{user.username}' HAS '{permission}' permission.")
        else:
            print(f"User '{user.username}' DOES NOT HAVE '{permission}' permission.")


    # Unknown command
    else:
        print("Unknown command.")