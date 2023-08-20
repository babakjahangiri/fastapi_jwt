from fastapi import FastAPI, HTTPException
from app.auth.jwt_handler1 import JWThandler


app = FastAPI()

users_db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register_user(username, name, email, role):
    # Check if the username is already taken
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already taken")


    # Store user information in the database
    users_db[username] = {
        "username": username,
        "name": name,
        "email": email,
        "role": role
    }

    # Generate and return JWT token for the registered user
    token = JWThandler.sign_jwt(username, name, email, role)
    return {"message": "User registered successfully", "token": token}
