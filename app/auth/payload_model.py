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
    iss: str
    sub: str
    name: str
    email: str
    role: str
    iat: datetime
    exp: datetime
    jti: str
    aud: Optional[str] = None  # Audience (Optional field, add more fields as necessary)
    # Add other fields if necessary.






# https://stackoverflow.com/questions/38897514/what-to-store-in-a-jwt


# {
#   "iss": "https://your-auth-server.com",  // Issuer
#   "sub": "1234567890",                     // Subject (usually the user ID)
#   "aud": "https://your-app.com",           // Audience (intended recipients)
#   "exp": 1629479163,                       // Expiration time (UNIX epoch time)
#   "nbf": 1629475563,                       // Not before (UNIX epoch time)
#   "iat": 1629475563,                       // Issued at (UNIX epoch time)
#   "jti": "aUniqueTokenId1234",             // JWT ID (to prevent the JWT from being replayed)
#   "roles": ["user", "admin"],              // Custom claim (roles for the user)
#   "email": "user@example.com",             // Custom claim (user's email)
#   "name": "John Doe"                       // Custom claim (user's name)
# }


# Best practices:

# Avoid Storing Sensitive Information: Don't put sensitive data in a JWT payload unless it's encrypted. JWTs are often just base64 encoded (not encrypted) and can be decoded by anyone who has the token.

# Use Standard Claims: Whenever possible, use standard claims (iss, sub, aud, exp, nbf, iat, jti) defined by the JWT specification.

# Keep It Small: Remember that a JWT is often included in an HTTP header. HTTP headers typically have a size limit (often configured on the server). So, don't add large amounts of data to a JWT.

# Use the "jti" Claim: This provides a unique identifier for the JWT which can be useful for preventing token reuse.

# Role-Based Access Control (RBAC): If you're using JWTs for authorization, you can include roles or permissions in the claims to indicate what the token bearer is allowed to do.

# Expiration Time: Always set an expiration time (exp) to ensure tokens aren't valid indefinitely. You can then use refresh tokens to get a new JWT if needed.

# Remember, this is a general-purpose example and the specific claims you need might differ based on your application and use-case. Always be cautious about the information you include and consult the relevant documentation or best practice guides for your specific implementation.
