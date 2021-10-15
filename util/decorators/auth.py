"""Module for Auth decorators"""
from flask import request

from errorHandler import MongoErrorHandler

def authenticated(func):
    """Auth Decorator to validate if the user is authenticated"""
    def inner():
        print(request.get_json())
        if request.get_json()["hello"] == "nice":
            raise MongoErrorHandler(
                "The user is saying hello, he is not validated", 404
            )
        response = func()
        return response

    return inner
