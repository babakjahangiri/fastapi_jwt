from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.jwt_handler import JWThandler


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.app = app

    async def dispatch_func(self, request: Request, call_next):
        authorization_header = request.headers.get("authorization")
        payload = None
        try:
            token = authorization_header.split()[1]
            jwt_handler = JWThandler()
            payload = jwt_handler.read_token(token)
        except:
            pass
        request.state.user = payload

        response = await call_next(request)
        return response
