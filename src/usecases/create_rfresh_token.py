from src.auth.jwt_handler import JWThandler , TokenType
from src.auth.payload_model import JWTPayload  


class CreateRefreshToken:
    def __init__(self) -> None:
        self.jwt_handler = JWThandler()

    def exectue(self,paylaod:JWTPayload):
        return self.jwt_handler.create_token(paylaod,TokenType.REFRESH_TOKEN)

    

