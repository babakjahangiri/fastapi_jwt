from src.db.user_db import fake_users_db


class Logout:
    def __init__(self) -> None:
        self.db = fake_users_db

    def execute(self, user_id_to_logout):
        user_info = self.db.get(user_id_to_logout)

        if user_info and "jti" in user_info and user_info["jti"] is not None:
            user_info["jti"] = None 
            return True, "User logged out successfully."
        else:
            return False, "No jti to invalidate or jti already invalid. Logout failed."    
