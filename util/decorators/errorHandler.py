"""Module for global error handling"""
from flask.json import jsonify


def exception_handler(func):
    """Handle all exceptions from routes"""

    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        # pylint: disable = broad-except
        except Exception as error:
            print(error)
            return format_and_return_error(error)

    inner.__name__ = func.__name__
    return inner


def format_and_return_error(error):
    """Format exception and return it as response"""
    status = getattr(error, "status", 500)
    message = getattr(error, "message", error.args)
    if type(message) == tuple and len(message) != 0:
        message = message[0]
    return {"message": message}, status


class MongoErrorHandler(Exception):
    """MongoErrorHandler for errors related to mongodb"""

    def __init__(self, message, status):
        Exception.__init__(self)
        self.message = message
        self.status = status
