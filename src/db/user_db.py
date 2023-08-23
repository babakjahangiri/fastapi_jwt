from uuid import uuid4
from pprint import pprint

fake_users_db = {
   "babak": {
        "username": "babak",
        "full_name": "Babak Jahangiri",
        "email": "babak@babak.uk",
        "plain_password": "babak1234",  # Plain password
        "hashed_password": "$2y$10$A6JeQdXR0.lymWDSzRuEW.LcIdjhi0aXmknfCnT0cfQF//dB/rUk2",
        "role": "admin",
        "disabled": False,
        "jti": "dfbe12ba-5a78-414e-9a00-8811c4e7954c" # Initialize jti as None
    },
    "arshiya": {
        "username": "arshiya",
        "full_name": "Arshiya Khalili",
        "email": "Arshiya@gmail.com",
        "plain_password": "arshiya",  # Plain password
        "hashed_password": "$2y$10$xevgOpWiwYXCZ1VXECSd/OptJE3Dq3Lo6wqFLhu7jN/zmw6Ir0WpS",
        "role": "user",
        "disabled": False,
        "jti": None  # Initialize jti as None
    },
    "anonymous": {
         "username": "anonymous",
        "full_name": "anonymous",
        "email": "anonymous@gmail.com",
        "plain_password": "anonymous",  # Plain password
        "hashed_password": "$2y$10$AQfbLRB0NxBvg.L0GMkgv.OV5RhXLK0PJ6sNH8FR0bz2LROUagWkq",
        "role": "user",
        "disabled": False,
        "jti": None  # Initialize jti as None
    },
}

# pprint(fake_users_db)