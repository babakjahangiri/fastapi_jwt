import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.jwt_handler import JWThandler
from app.auth.payload_model import RoleType
from app.db.user_db import fake_users_db

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = JWThandler.decodeJWT(token)
    return {"username": payload["sub"]}


@app.get("/secure")
def secure():
    return {"this is a secure content"}


@app.post("/token")
def register_user(username, name, email, role):
    # Check if the username is already taken
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already taken")


@app.post("/register")
def register_user(username, password, name, email, role: RoleType):
    # Check if the username is already taken
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already taken")

    password = password.encode("utf-8")
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt and the generated salt
    hashed_password = bcrypt.hashpw(password, salt)

    # Store user information in the database
    fake_users_db[username] = {
        "username": username,
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "role": RoleType.USER.value.lower(),
        "disabled": False,
    }

    print(f"salt ----> : {salt}")
    print(f"hashed_password ----> : {hashed_password}")

    if bcrypt.checkpw(password, hashed_password):
        print("Password is correct!")
    else:
        print("Password is incorrect!")

    # Generate and return JWT token for the registered user
    token = JWThandler.sign_jwt(username, name, email, role)
    return {"message": "User registered successfully", "token": token}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not JWThandler.verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = JWThandler.signJWT(username)
    return JWThandler.token_response(token)
