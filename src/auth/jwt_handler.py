from datetime import datetime, timedelta
from enum import Enum

import jwt

from src.auth.payload_model import JWTPayload


class TokenType(str, Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"


class JWThandler:
    _SECRET_KEY = "super-secret-key"
    _ALGORITHM = "HS256"
    _ACCESS_TOKEN_EXPIRE = 60 * 60 * 24  # shorter
    _REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 7  # longer

    def create_token(self, payload_model: JWTPayload, token: TokenType):
        current = datetime.utcnow()

        match token:
            case TokenType.ACCESS_TOKEN:
                exp_datetime = current + timedelta(seconds=self._ACCESS_TOKEN_EXPIRE)
            case TokenType.REFRESH_TOKEN:
                exp_datetime = current + timedelta(seconds=self._REFRESH_TOKEN_EXPIRE)
            case _:
                exp_datetime = current

        payload = payload_model.asdict()
        payload["exp"] = int(exp_datetime.timestamp())
        payload["typ"] = TokenType.ACCESS_TOKEN.value.lower()

        return jwt.encode(payload, self._SECRET_KEY, algorithm=self._ALGORITHM)

    def read_token(self, token: str) -> dict[str, any]:
        try:
            return jwt.decode(token, self._SECRET_KEY, algorithms=self._ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise ValueError("Signature has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid JWT token.")


# Explanation:

# JWThandler now has the verify_password method leveraging passlib to verify a hashed password.
# The users_db mock "database" contains a bcrypt hashed password for alice (which is "password").
# The /token route uses FastAPI's built-in OAuth2PasswordRequestForm to gather the username and password.
# The oauth2_scheme is an instance of OAuth2PasswordBearer, which provides a way to get the token from the request (typically the Authorization header).
# The protected_route function uses Depends(oauth2_scheme) to retrieve the token and then decodes it to verify.
# Note:

# This example demonstrates JWT-based authentication with password hashing but doesn't implement a full OAuth flow.
# In real-world applications, always keep secrets, keys, and passwords out of the code, preferably in environment variables.
# While this example uses an in-memory mock "database", in real applications, you'd fetch users and their hashed passwords from an actual database.
