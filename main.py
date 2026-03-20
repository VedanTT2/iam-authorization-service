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
print("add_parent <child_role_id> <parent_role_id>")
print("describe_user <user_id>")
print("show_roles")
print("why_user_has_permission <user_id> <permission>")
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
            user_store.save_users()

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

    elif action == "add_parent":

        if len(parts) != 3:
            print("Usage: add_parent <child_role_id> <parent_role_id>")
            continue

        child_role_id = int(parts[1])
        parent_role_id = int(parts[2])

        try:
            role_store.add_parent_to_role(child_role_id, parent_role_id)
            print(f"Role {child_role_id} now inherits role {parent_role_id}.")
        except ValueError as e:
            print(f"Error: {e}")

    # DESCRIBE USER
    elif action == "describe_user":

        if len(parts) != 2:
            print("Usage: describe_user <user_id>")
            continue

        user_id = int(parts[1])
        user = user_store.get_user(user_id)

        if not user:
            print("User not found.")
            continue

        print(f"User: {user.username}")
        print(f"User ID: {user.user_id}")

        print("\nAssigned Roles:")
        if not user.role_ids:
            print("- No roles assigned")
        else:
            all_permissions = set()

            for role_id in user.role_ids:
                role = role_store.get_role(role_id)

                if role:
                    print(f"- {role.name} (ID: {role.role_id})")
                    all_permissions.update(role.get_all_permissions(role_store))
                else:
                    print(f"- Unknown Role (ID: {role_id})")

            print("\nEffective Permissions:")
            if all_permissions:
                for permission in sorted(all_permissions):
                    print(f"- {permission}")
            else:
                print("- No permissions found")

    # Show role graph
    elif action == "show_roles":

        print("\nRole Hierarchy\n")

        roles = role_store.get_all_roles()

        role_map = {role.role_id: role for role in roles}

        # build child mapping
        children = {}

        for role in roles:
            for parent_id in role.parent_roles:
                children.setdefault(parent_id, []).append(role.role_id)

        for role in roles:
            if role.role_id not in children:
                continue

            print(f"{role.name} ({role.role_id})")

            for child_id in children[role.role_id]:
                child = role_map.get(child_id)
                if child:
                    print(f" └ {child.name} ({child.role_id})")

            print()

    # WHY USER HAS PERMISSION
    elif action == "why_user_has_permission":

        if len(parts) != 3:
            print("Usage: why_user_has_permission <user_id> <permission>")
            continue

        user_id = int(parts[1])
        permission = parts[2].lower()

        user = user_store.get_user(user_id)

        if not user:
            print("User not found.")
            continue

        found = False

        for role_id in user.role_ids:
            role = role_store.get_role(role_id)

            if role:
                path = role.find_permission_path(permission, role_store)

                if path:
                    print(f"\nUser {user.username} has permission '{permission}'\n")
                    print("Path:")
                    print(f"{user.username} -> " + " -> ".join(path))
                    found = True
                    break

        if not found:
            print(f"User {user.username} does NOT have permission '{permission}'")


    # Unknown command
    else:
        print("Unknown command.")