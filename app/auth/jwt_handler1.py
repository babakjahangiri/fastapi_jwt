import datetime
import uuid

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
users_db = {
    "alice": {
        "hashed_password": "$2b$12$K.bAyVLZl6LXqlHHpS8A1eK.VX20TgI4AVnq3D0a0KSlOGy3TxHxe"
    }
}


class JWThandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def signJWT(username: str):
        jti = str(uuid.uuid4())
        expiration = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "exp": expiration,
            "iat": datetime.datetime.utcnow(),
            "sub": username,
            "jti": jti,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decodeJWT(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise JWTError
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    def token_response(token: str):
        return {"access_token": token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not JWThandler.verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = JWThandler.signJWT(username)
    return JWThandler.token_response(token)


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = JWThandler.decodeJWT(token)
    return {"username": payload["sub"]}


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
