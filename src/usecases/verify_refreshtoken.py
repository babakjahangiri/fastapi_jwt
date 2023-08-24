from src.db.user_db import fake_users_db
from src.auth.jwt_handler import JWThandler , TokenType
from src.exceptions import InvalidTokenError , UserNotFound

class VerifyRefreshtoken:
    def __init__(self):
        self.db = fake_users_db
        self.jwt_handler = JWThandler()

    def execute(self, refresh_token: str):
        try:
            payload = self.jwt_handler.read_token(refresh_token)
        except InvalidTokenError:
            raise InvalidTokenError("Invalid refresh token")

        username = payload["sub"]
        user_info = self.db.get(username)

        if user_info is None:
            raise UserNotFound()

        stored_refresh_token = user_info.get("refresh_token")

        if stored_refresh_token != refresh_token:
            raise InvalidTokenError("Refresh token mismatch")

        return True, "Refresh token is valid"