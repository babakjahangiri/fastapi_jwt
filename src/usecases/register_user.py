from src.db.user_db import fake_users_db
from src.exceptions import UsernameAlreadyExistsError
from src.auth.password_context import PasswordContext

class RegisterUser:
    def __init__(self) -> None:
        self.db = fake_users_db
        
        
        self.password_context = PasswordContext()

    def execute(self, data: dict[str, str]) -> None:
        # Check if the username is already taken
        if data["username"] in fake_users_db:
            raise UsernameAlreadyExistsError(data["username"])

        password = data["password"].encode("utf-8")
        # Generate a salt

        # Hash the password using bcrypt and the generated salt
        hashed_password = self.password_context.hash_password(password)

        # Store user information in the database
        fake_users_db[data["username"]] = {
            "username": data["username"],
            "name": data["name"],
            "email": data["email"],
            "hashed_password": hashed_password,
            "role": data["role"],
            "disabled": False,
        }
 

