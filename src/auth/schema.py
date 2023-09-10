from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    email: str
    role: str
    disabled: bool
