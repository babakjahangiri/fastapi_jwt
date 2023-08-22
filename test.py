from src.auth.jwt_handler import JWThandler, TokenType
from src.auth.payload_model import JWTPayload, RoleType

payload = JWTPayload(
    "rfe4t4b2f-ca4c-544f-92a2", "Arshia", "arshia@gmail.com", RoleType.ADMIN
)


jwthnler = JWThandler()
my_access_token = jwthnler.create_token(payload, TokenType.ACCESS_TOKEN)


print(jwthnler.read_token(my_access_token))


# from fastapi import Depends, FastAPI, HTTPException, Security
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
