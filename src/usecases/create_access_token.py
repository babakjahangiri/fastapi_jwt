from src.auth.jwt_handler import JWThandler , TokenType
from src.auth.payload_model import JWTPayload  


class CreateAccessToken:
    def __init__(self) -> None:
        self.jwt_handler = JWThandler()

    def exectue(self,paylaod:JWTPayload):
        return self.jwt_handler.create_token(paylaod,TokenType.ACCESS_TOKEN)

    

