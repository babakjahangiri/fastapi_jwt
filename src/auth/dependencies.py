from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWKError

from src.auth.jwt_handler import JWThandler
from src.auth.schema import User
from src.db.user_db import fake_users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='invalid credentials',
    headers={'WWW-Authenticate': 'bearer'}
)


class ParseToken:
    def __init__(self, token: Annotated[str, Depends(oauth2_scheme)]):
        jwt_handler = JWThandler()
        try:
            self.payload = jwt_handler.read_token(token)
        except PyJWKError:
            raise CREDENTIALS_EXCEPTION


class CurrentUser:
    def __init__(self, parse_token: ParseToken = Depends()):
        username: str = parse_token.payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION

        user = fake_users_db.get(username)
        if user is None:
            raise CREDENTIALS_EXCEPTION

        self.user = User(**user)


class CurrentActiveUser:
    def __init__(self, current_user: CurrentUser = Depends(CurrentUser)):
        if current_user.user.disabled:
            raise CREDENTIALS_EXCEPTION
        self.user = current_user.user



