class UserService:
    '''service layer responsible for user--related business logic.
    handles validation and coordination between user and RoleStore'''

    def __init__(self, role_store):
        self.role_store = role_store

    def assign_role_to_user(self, user, role_id):
        role = self.role_store.get_role(role_id)

        if not role:
            raise ValueError(f"Role ID{role_id} does not exist")
        user.role_ids.add(role_id)

    def user_has_permission(self, user, permission):
        for role_id in user.role_ids:
            role = self.role_store.get_role(role_id)

            if role:

                all_permissions = role.get_all_permissions(self.role_store)

                if permission in all_permissions:
                    return True
        return False

