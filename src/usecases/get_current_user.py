from src.db.user_db import fake_users_db
from src.auth.jwt_handler import JWThandler
from fastapi import HTTPException , status ,Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWKError



class GetCurrentLoggedInUser:
    def __init__(self):
        self.db = fake_users_db

    def execute(self, user: dict | None):
        error_credential = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials',
            headers={'WWW-Authenticate': 'bearer'}
        )

        if not user:
            raise error_credential
            
        username = user.get('sub')
        if not username:
            raise error_credential

        user_obj = self.db.get(username)
        if user_obj is None:
            raise error_credential

        return user_obj
