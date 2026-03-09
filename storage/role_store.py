from models.role import Role

class RoleStore:   # acts like an in memory db for storing roles

    def __init__(self):
        self.roles = {}  # Dict to store roles, key = roleID, value =  role object


    def add_role(self, role):           # add role object to the store
        self.roles[role.role_id] = role


    def get_role(self, role_id):        # getting a role by its ID, return None if not found
        return self.roles.get(role_id)


    def remove_role(self, role_id):     # remove a role from the store
        if role_id in self.roles:
            del self.roles[role_id]



