from src.db.user_db import fake_users_db
from src.auth.password_context import PasswordContext
from src.exceptions import UserNotFound



class ResetPassword:
    def __init__(self) -> None:
        self.db = fake_users_db
        self.password_context = PasswordContext()


    def execute(self,username:str,current_password:str,new_password:str=None):
        user_info = self.db.get(username)


        if user_info is None:
            raise UserNotFound()
        

        stored_password = user_info.get("plain_password")


        if stored_password != current_password:
            return False,"Incorrect password"
        elif new_password:
            hashed_ppassword = self.password_context.hash_password(new_password)
            user_info["hashed_password"] = hashed_ppassword
        return True,new_password
            





