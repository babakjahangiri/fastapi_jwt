from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.jwt_handler import JWThandler
from src.auth.payload_model import RoleType
from src.exceptions import UsernameAlreadyExistsError
from src.usecases.get_current_user import GetCurrentLoggedInUser
from src.usecases.login import Login
from src.usecases.logout import Logout
from src.usecases.register_user import RegisterUser

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = JWThandler.decodeJWT(token)
    return {"username": payload["sub"]}


@app.get("/admin")
def admin_route():
    return {"this path is available only for admins"}


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

    register_user = RegisterUser()

    try:
        register_user.execute(user_data)
        return {"message": "User register successfully", "user_inofo": user_data}
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    login_user = Login()

    username = form_data.username
    password = form_data.password

    result = login_user.execute(username, password)
    return result


@app.post("/verify")
def verify():
    pass


@app.post("/refresh")
def refresh():
    pass


@app.get("/logout")
def logout():
    logout_usecase = Logout()
    logout_usecase.execute()

    return {"message": "Logged out successfully"}


@app.get("/me")
def get_current_user(authorization: str = Header()):
    print(f"Authorization header: {authorization}")

    try:
        token = authorization.split("Bearer ")[1]
        print(f"Extracted token: {token}")
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    current_user_usecase = GetCurrentLoggedInUser()
    user_info = current_user_usecase.execute(token)

    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_info
