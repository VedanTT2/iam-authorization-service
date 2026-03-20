from models.user import User
from storage.json_storage import load_json, save_json

class UserStore:
    def __init__(self, file_path = "data/users.json"):
        self.file_path = file_path
        self.users = {}

        users_data = load_json(self.file_path)

        for user_data in users_data:
            user = User.from_dict(user_data)
            self.users[user.user_id] = user

    def add_user(self, user):
        if user.user_id in self.users:
            return False
        self.users[user.user_id] = user
        self._save_users()
        return True

    def get_user(self, user_id):
        return self.users.get(user_id,)

    def get_all_users(self):
        return list(self.users.values())

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self._save_users()

    def _save_users(self) -> None:
        users_data = [user.to_dict() for user in self.users.values()]
        save_json(self.file_path, users_data)


