class User:
    def __init__(self, user_id, username, role_ids = None):  # Initialize user with user_id: unique identity
        self.user_id = user_id              # role_ids: set of role ids assigned to a user
        self.username = username
        self.role_ids = set(role_ids) if role_ids is not None else set()


    def assign_role(self, role_id,):     # Assign role to a user by ID
        self.role_ids.add(role_id)


    def remove_role(self, role_id):      # discard() used to avoid error if no role found
        self.role_ids.discard(role_id)

    def to_dict(self):
        return {"user_id": self.user_id,
                "username": self.username,
                "role_ids": list(self.role_ids)
                }

    @classmethod
    def from_dict(cls, d):
        return cls(
            data["user_id"],
            data["username"],
            data.get("role_ids", []),
        )

