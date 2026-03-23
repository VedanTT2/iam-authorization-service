class UserService:
    """Service layer responsible for user-related business logic.
    Handles validation and coordination between User and RoleStore.
    Also maintains a permission cache for faster permission checks.
    """

    def __init__(self, role_store):
        self.role_store = role_store

        # Cache format:
        # {
        #     user_id: {"read", "write", "delete"}
        # }
        self.user_permission_cache = {}

    def assign_role_to_user(self, user, role_id):
        role = self.role_store.get_role(role_id)

        if not role:
            raise ValueError(f"Role ID {role_id} does not exist")

        user.role_ids.add(role_id)

        # User's permissions may have changed, so clear cache
        self.invalidate_user_cache(user.user_id)

    def invalidate_user_cache(self, user_id):
        """Remove one user's cached permissions if present."""
        if user_id in self.user_permission_cache:
            del self.user_permission_cache[user_id]

    def build_user_permission_cache(self, user):
        """Compute all effective permissions for a user and store them in cache."""
        all_permissions = set()

        for role_id in user.role_ids:
            role = self.role_store.get_role(role_id)

            if role:
                all_permissions.update(role.get_all_permissions(self.role_store))

        self.user_permission_cache[user.user_id] = all_permissions
        return all_permissions

    def get_user_permissions(self, user):
        if user.user_id not in self.user_permission_cache:
            print("[CACHE MISS] Building permissions...")
            return self.build_user_permission_cache(user)

        print("[CACHE HIT] Using cached permissions...")
        return self.user_permission_cache[user.user_id]

    def user_has_permission(self, user, permission):
        permission = permission.lower()

        cached_permissions = self.get_user_permissions(user)
        return permission in cached_permissions