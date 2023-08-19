import datetime
import uuid

import jwt
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
users = {"alice": {"password": "alicepassword"}}


class JWThandler:
    @staticmethod
    def signJWT(user: str):
        jti = str(uuid.uuid4())
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            "exp": expiration,  # iser id +mongodb id
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow(),  # expiration timestamp
            "sub": user,
            "jti": jti,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decodeJWT(token: str):
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_jwt
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def token_response(token: str):
        return {"access_token": token, "token_type": "bearer"}


@app.post("/token")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        token = JWThandler.signJWT(username)
        return JWThandler.token_response(token)

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/protected")
def protected_route(user=Depends(JWThandler.decodeJWT)):
    return {"message": f"Hello {user['sub']}"}
