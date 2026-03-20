class Role:
    def __init__(self, role_id, name):  # Initialize roles with a unique ID "role_id",
        self.role_id = role_id          # name: Human readable role name
        self.name = name                # permissions: A set to store unique permissions
        self.permissions = set()
        self.parent_roles = set()       # Parent_role: A set to store all parent role


    def add_permission(self, permission):   # add permissions to the roles like read write etc.
        self.permissions.add(permission.lower())


    def remove_permission(self, permission):    # remove permission if existed,
        self.permissions.discard(permission.lower())    # discard it to avoid error if permission does not exist


    def has_permission(self, permission, role_store = None):    # to check a specific permission and return true or false
        permission = permission.lower()

        if role_store is None:
            return permission in self.permissions
        return permission in self.get_all_permissions(role_store)

    def add_parent_role(self, parent_role_id):
        self.parent_roles.add(parent_role_id)

    def inherits_from(self, target_role_id, role_store, visited = None):
        #'''Return True if current role directly or indirectly inherits from target_role_id. used to prevent cycles while assigning parent roles'''
        if visited is None:
            visited = set()

        if self.role_id in visited:
            return False
        visited.add(self.role_id)

        if target_role_id in self.parent_roles:
            return True

        for parent_role_id in self.parent_roles:
            parent_role = role_store.get_role(parent_role_id)
            if parent_role and parent_role.inherits_from(target_role_id, role_store, visited):
                return True

        return False

    def get_all_permissions(self, role_store, visited=None):
        if visited is None:
            visited = set()

        if self.role_id in visited:
            return set()
        visited.add(self.role_id)

        all_permissions = set(self.permissions)

        for parent_role_id in self.parent_roles:
            parent_role = role_store.get_role(parent_role_id)
            if parent_role:
                all_permissions.update(parent_role.get_all_permissions(role_store, visited))
        return all_permissions

    def find_permission_path(self, permission, role_store, visited=None):
        """
        Returns the inheritance path showing why this role has a permission.
        Example return: ["Admin", "Viewer", "read"]
        """
        permission = permission.lower()

        if visited is None:
            visited = set()

        if self.role_id in visited:
            return None

        visited.add(self.role_id)

        if permission in self.permissions:
            return [self.name, permission]

        for parent_role_id in self.parent_roles:
            parent_role = role_store.get_role(parent_role_id)
            if parent_role:
                path = parent_role.find_permission_path(permission, role_store, visited)
                if path:
                    return [self.name] + path

        return None


    def to_dict(self):
        return {"role_id": self.role_id,
                "name": self.name,                  # convert role object to dict
                "permissions": list(self.permissions),
                "parent_roles": list(self.parent_roles)}


    @staticmethod
    def from_dict(data):
        role = Role(data["role_id"], data["name"])
        role.permissions = set(data.get("permissions", []))
        role.parent_roles = set(data.get("parent_roles", []))
        return role