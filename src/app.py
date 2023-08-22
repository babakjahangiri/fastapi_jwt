from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.jwt_handler import JWThandler
from src.auth.payload_model import RoleType
from src.exceptions import UsernameAlreadyExistsError
from src.usecases.register_user import RegisterUser
from src.usecases.login import Login

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


@app.post("/register")
def register_user(username, password, name, email, role: RoleType):
    user_data = {
        "username": str(username),
        "password": str(password),
        "name": str(name),
        "email": str(email),
        "role": str(
            role.value.lower()
        ),  # Convert the RoleType enum to its string representation
    }

    print(user_data)

    register_user = RegisterUser()

    try:
        register_user.execute(user_data)
        return {"message":"User register successfully","user_inofo":user_data}
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # print(f"salt ----> : {salt}")
    # print(f"hashed_password ----> : {hashed_password}")

    # if bcrypt.checkpw(password, hashed_password):
    #     print("Password is correct!")
    # else:
    #     print("Password is incorrect!")

    # # Generate and return JWT token for the registered user
    # token = JWThandler.sign_jwt(username, name, email, role)
    # return {"message": "User registered successfully", "token": token}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    login_user = Login()

    username = form_data.username
    password = form_data.password

    result = login_user.execute(username,password)
    return result

