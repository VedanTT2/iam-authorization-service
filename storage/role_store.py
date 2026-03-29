from models.role import Role
from storage.json_storage import load_json, save_json

class RoleStore:
    def __init__(self, file_path = "data/roles.json"):  # constructor runs when RoleStore obj is created
        self.file_path = file_path      # files where roles will be stored

        self.roles = {}     # dict to store roles in memory, key = role_id, value = role obj

        roles_data = load_json(self.file_path)    # load roles from json file

        for role_data in roles_data:           # roles_data is list of dict
            role = Role.from_dict(role_data)   # i convert each dict into role obj
            self.roles[role.role_id] = role     # store role obj in dict

    def add_role(self, role):
        if role.role_id in self.roles:
            return False

        self.roles[role.role_id] = role
        self._save_roles()
        return True             # save updated roles to JSON file


    def get_role(self, role_id):        # get a role using role_id
        return self.roles.get(role_id)  # # return role obj if found, otherwise return none

    def remove_role(self, role_id):
        if role_id in self.roles:
            del self.roles[role_id]
            self._save_roles()

    def add_parent_to_role(self, child_role_id, parent_role_id):
        child_role = self.get_role(child_role_id)
        parent_role = self.get_role(parent_role_id)

        if not child_role:
            raise ValueError(f"Child role ID {child_role_id} does not exist")

        if not parent_role:
            raise ValueError(f"Parent role ID {parent_role_id} does not exist")

        if child_role_id == parent_role_id:
            raise ValueError("A role cannot inherit from itself")

        # If parent already inherits from child, adding this link creates a cycle
        if parent_role.inherits_from(child_role_id, self):
            raise ValueError(f"Cannot add parent role '{parent_role_id}' to '{child_role_id}' because it creates a cycle ")

        child_role.add_parent_role(parent_role_id)
        self._save_roles()


    def get_all_roles(self):
        return list(self.roles.values())

    def _save_roles(self):
        roles_data = [role.to_dict() for role in self.roles.values()]  # convert all role obj into dict
        save_json(self.file_path, roles_data)    # store it in json file

    def add_permission_to_role(self, role_id, permission):
        role = self.get_role(role_id)

        if not role:
            raise ValueError(f"Role ID {role_id} does not exist")

        role.add_permission(permission)
        self._save_roles()
        return role

    def add_deny_permission_to_role(self, role_id, permission):
        role = self.get_role(role_id)

        if not role:
            raise ValueError(f"Role ID {role_id} does not exist")

        role.add_deny_permission(permission)
        self._save_roles()
        return role

    def remove_permission_from_role(self, role_id, permission):
        role = self.get_role(role_id)

        if not role:
            raise ValueError(f"Role ID {role_id} does not exist")

        if permission not in role.permissions:
            return None

        role.permissions.remove(permission)
        self._save_roles()
        return role