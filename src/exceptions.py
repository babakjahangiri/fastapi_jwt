class FastAPTJWTException(Exception):
    """
    Base except which all fastapi_jwt errors extend
    """

    pass


class AccessTokenRequired(FastAPTJWTException):
    """
    Error raised when a valid, non-access JWT attempt to access an endpoint
    protected by jwt_required, jwt_optional, fresh_jwt_required
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class RefreshTokenRequired(FastAPTJWTException):
    """
    Error raised when a valid, non-refresh JWT attempt to access an endpoint
    protected by jwt_refresh_token_required
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class UsernameAlreadyExistsError(FastAPTJWTException):
    def __init__(self, status_code: int, message: str = "Username already exists"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class LoginFailedError(FastAPTJWTException):
    def __init__(self, status_code: int = 401, message: str = "Login Failed due to incorrect username or password"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class UserNotFound(FastAPTJWTException):
    def __init__(self, status_code: int = 404, message: str = "User Not found"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
