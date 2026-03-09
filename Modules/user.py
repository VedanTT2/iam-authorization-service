class User:
    def __init__(self, user_id, username):  # Initialize user with user_id: unique identity
        self.user_id = user_id              # role_ids: set of role ids assigned to a user
        self.username = username
        self.role_ids = set()


    def assign_role(self, role_id, role_store):     # Assign role to a user by ID
        self.role_ids.add(role_id)


    def remove_role(self, role_id):      # discard() used to avoid error if no role found
        self.role_ids.discard(role_id)


