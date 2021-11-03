"""Module for Auth decorators"""
from datetime import datetime, timedelta
from http import HTTPStatus

from flask import request
from jwt import encode, decode, PyJWTError

from models.User import User

JWT_PRIVATE_KEY = "secret"

DEFAULT_TOKEN_EXPIRATION_DAYS = 30


class AuthenticationFailed(Exception):
    """Failed to Authenticate User"""

    status = HTTPStatus.UNAUTHORIZED


def authenticated(func):
    """Auth Decorator to validate if the user is authenticated"""

    def inner(*args, **kwargs):
        # Get auth header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationFailed("Missing Authorization header")

        # Check Bearer auth
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header missing keyword Bearer")

        # Verify auth token
        auth_token = auth_header.split("Bearer ")[1]
        try:
            data = decode(auth_token, JWT_PRIVATE_KEY, algorithms=["HS256"])
        except PyJWTError as err:
            raise AuthenticationFailed(f"Invalid signature: {err}") from err

        # Get user associated with the token
        user = User.get_by_id(data["id"])
        kwargs["current_user"] = user
        return func(*args, **kwargs)

    inner.__name__ = func.__name__
    return inner


def generate_auth_token(user: User, expiration=DEFAULT_TOKEN_EXPIRATION_DAYS):
    """Returns an auth token for given user"""
    now = datetime.now()
    expiry = now + timedelta(days=expiration)
    jwt_claim = {
        "fname": user.firstName,
        "lname": user.lastName,
        "email": user.email,
        "uname": user.username,
        "id": user.get_id(),
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
    }
    encoded_jwt = encode(jwt_claim, JWT_PRIVATE_KEY, algorithm="HS256")
    return encoded_jwt
