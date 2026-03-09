class Role:
    def __init__(self, role_id, name):  # Initialize roles with a unique ID "role_id",
        self.role_id = role_id          # name: Human readable role name
        self.name = name                # permissions: A set to store unique permissions
        self.permissions = set()


    def add_permission(self, permission):   # add permissions to the roles like read write etc.
        self.permissions.add(permission.lower())


    def remove_permission(self, permission):    # remove permission if existed,
        self.permissions.discard(permission.lower())    # discard it to avoid error if permission does not exist


    def has_permission(self, permission):           # to check a specific permission and return true or false
        return permission.lower() in self.permissions