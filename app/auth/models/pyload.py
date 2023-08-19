#  payload = {
#             "exp": expiration,
#             "iat": datetime.datetime.utcnow(),
#             "sub": user,
#             "jti": jti,
#         }


from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JWTPayload:
    sub: str
    name: str
    email: str
    role: str
    iat: datetime
    exp: datetime
    jti: str
    aud: Optional[str] = None  # Audience (Optional field, add more fields as necessary)
    iss: Optional[str] = None  # Issuer (Optional field)
    # Add other fields if necessary.


# https://stackoverflow.com/questions/38897514/what-to-store-in-a-jwt
