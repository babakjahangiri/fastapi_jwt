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


def parse_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    jwt_handler = JWThandler()
    try:
        return jwt_handler.read_token(token)
    except PyJWKError:
        raise CREDENTIALS_EXCEPTION


def get_current_user(payload: dict = Depends(parse_token)) -> User:
    username: str = payload.get("sub")
    if username is None:
        raise CREDENTIALS_EXCEPTION

    user = fake_users_db.get(username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return User(**user)


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if user.disabled:
        raise CREDENTIALS_EXCEPTION
    return user
