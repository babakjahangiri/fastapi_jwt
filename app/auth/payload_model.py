import uuid
from dataclasses import dataclass, field
from enum import Enum


class RoleType(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class JWTPayload:
    iss: str
    sub: str
    iat: int
    exp: int
    jti: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # Name of the user
    email: str  # Email of the user
    role: RoleType  # Role of the user


# Issuer : It should be the URL of the authentication server that generated the token. This helps the recipient verify the source of the token.
# Subject: This claim identifies the subject of the JWT, typically representing the user's unique identifier (such as user ID). It's used to specify whom the JWT is about.
# NOTE : iat and exp stored as epochtime often called "Unix time" or "POSIX time," refers to the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT)
# Epoch time, when referring to Unix time, is typically represented as a signed 32-bit integer. The maximum value of a signed 32-bit integer 2,147,483,647.
# "jti" (JWT ID): This claim provides a unique identifier for the JWT. It can be used to prevent JWT replay attacks, where an attacker uses the same token multiple times.
