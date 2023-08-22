from src.db.user_db import fake_users_db
from src.auth.jwt_handler import JWThandler

class GetCurrentLoggedInUser:
    def __init__(self):
        self.db = fake_users_db
        self.jwt_handler = JWThandler()

    def execute(self, token: str):
        payload = self.jwt_handler.read_token(token)
        print(f'{payload}')
        print(token)
        username = payload['sub']
        return self.db.get(username)
