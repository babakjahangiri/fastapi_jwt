from src.db.user_db import fake_users_db
from src.exceptions import UserNotFound , UsernameAlreadyExistsError , LoginFailedError
from src.auth.password_context import PasswordContext


class Login:
    def __init__(self) -> None:
        self.db = fake_users_db
        self.password_context = PasswordContext()

    def execute(self,username:str,password:str) -> dict:
        user_info = self.db.get(username)



        if user_info is None:
            raise UserNotFound()
        
        hash_password = user_info["hashed_password"]


        if self.password_context.verify_password(password,hash_password):
            return {"message":"Login successfully","user_info":user_info}
        else:
            raise LoginFailedError()