# Convert UNIX Timestamp to Python's datetime:

# The UNIX timestamps from the JWT are integers representing seconds since the epoch. Convert these to Python's datetime objects:


import datetime

import jwt

encoded_jwt = "your_jwt_token_here"
decoded_payload = jwt.decode(encoded_jwt, options={"verify_signature": False})


iat_datetime = datetime.datetime.utcfromtimestamp(decoded_payload["iat"])
exp_datetime = datetime.datetime.utcfromtimestamp(decoded_payload["exp"])


jwt_collection = db["jwt_payloads"]

stored_payload = jwt_collection.find_one({"jti": decoded_payload["jti"]})

if stored_payload:
    if stored_payload["iat"] == iat_datetime:
        print("Issued At matches!")
    if stored_payload["exp"] == exp_datetime:
        print("Expiration matches!")


# Notes:

# Ensure you're using utcfromtimestamp and not just fromtimestamp, as JWTs typically use UTC for iat and exp, and so does MongoDB by default.
# The process of converting the UNIX timestamp to a datetime object is essential to ensure type compatibility between your JWT and MongoDB, allowing for correct date-based operations and comparisons.
# If you're performing any security-sensitive operations, remember to verify the JWT's signature and handle any potential exceptions or errors in the decoding process.
