from flask import request

from util.decorators.errorHandler import MongoErrorHandler

def authenticated(func):
    def inner(*args, **kwargs):
        print(request.get_json())
        if request.get_json()["hello"] == 'nice':
            raise MongoErrorHandler("The user is saying hello, he is not validated", 404)
        response = func()
        return response
    return inner