from src.db.user_db import fake_users_db


class Logout:
    def __init__(self) -> None:
        self.db = fake_users_db

    def execute(self) -> None:
        pass
