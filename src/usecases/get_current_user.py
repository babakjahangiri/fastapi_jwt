from src.db.user_db import fake_users_db
from src.auth.jwt_handler import JWThandler
from fastapi import HTTPException , status ,Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWKError



class GetCurrentLoggedInUser:
    def __init__(self):
        self.db = fake_users_db
        self.jwt_handler = JWThandler()

    def execute(self,token:str):
        error_credential = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials',
            headers={'WWW-Authenticate': 'bearer'}
        )

        try:
            payload = self.jwt_handler.read_token(token)
            username = payload.get('sub')
            if not username:
                raise error_credential
        except PyJWKError:
            raise error_credential

        user = self.db.get(username)
        if user is None:
            raise error_credential

        return user
