from src.db.user_db import fake_users_db
from src.exceptions import UserNotFound , UsernameAlreadyExistsError , LoginFailedError
from src.auth.password_context import PasswordContext
from src.auth.jwt_handler import TokenType
from src.auth.payload_model import JWTPayload
from src.auth.jwt_handler import JWThandler
class Login:
    def __init__(self) -> None:
        self.db = fake_users_db
        self.password_context = PasswordContext()
        self.jwt_handler = JWThandler()

        

    def execute(self,username:str,password:str) -> dict:
        user_info = self.db.get(username)

        password_encode = password.encode("utf-8")

        if user_info is None:
            raise UserNotFound()
        
        hash_password = user_info["hashed_password"]

        
        if self.password_context.verify_password(password_encode, hash_password):
            payload_model = JWTPayload(
                sub=username,
                name=user_info["full_name"],
                email=user_info["email"],
                role=user_info["role"]
            )

            access_token = self.jwt_handler.create_token(payload_model, TokenType.ACCESS_TOKEN)
            refresh_token = self.jwt_handler.create_token(payload_model, TokenType.REFRESH_TOKEN)

            return {
                "message": "Login successfully",
                "user_info": user_info,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            raise LoginFailedError()


