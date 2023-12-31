import secrets
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.dependencies import CurrentActiveUser
from src.auth.jwt_handler import JWThandler
from src.auth.payload_model import RoleType
from src.auth.schema import User
from src.dependencies import get_current_active_user
from src.exceptions import UsernameAlreadyExistsError,UserNotFound
from src.usecases.get_current_user import GetCurrentLoggedInUser
from src.usecases.login import Login
from src.usecases.logout import Logout
from src.usecases.register_user import RegisterUser
from src.usecases.reset_password import ResetPassword
from src.usecases.verify_refreshtoken import VerifyRefreshtoken


app = FastAPI()

user_csrf_tokens = {}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_csrf_token(request: Request, user_token: str = None):
    received_token = request.headers.get("X-CSRF-Token", user_token)
    
    if received_token not in user_csrf_tokens.values():
        raise HTTPException(status_code=400, detail="Invalid CSRF Token")
    
    return received_token


@app.get("/")
def read_root():
    return {"Hello": "World"}



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
def logout(user:str):

    logout_use_case = Logout()
    return logout_use_case.execute(user)
    
  
@app.get("/me", response_model=User)
def get_current_user(user: User = Depends(get_current_active_user)):
    return user
  
#def get_current_user(active_user: CurrentActiveUser = Depends()):
#    return active_user.user





@app.post("/reset-password")
def reset_password(userame:str,current_password:str, new_password:str):
    rest_user_password = ResetPassword()
    return rest_user_password.execute(userame,current_password,new_password)




@app.post("/verify-refresh-token")
def verify_refresh_token(token: str):
    verify_token = VerifyRefreshtoken()
    return verify_token.execute(token)



@app.get("/generate-csrf-token")
def generate_csrf_token(response: Response):
    user_id = "some_user_id"  
    csrf_token = secrets.token_hex(16)
    user_csrf_tokens[user_id] = csrf_token
    
    response.set_cookie(key="csrf_token", value=csrf_token, samesite="lax", httponly=True)
    return {"message": "CSRF token generated and set as cookie"}

@app.post("/some-endpoint")
def protected_endpoint(token: str = Depends(validate_csrf_token)):
    return {"message": "Request processed successfully"}
