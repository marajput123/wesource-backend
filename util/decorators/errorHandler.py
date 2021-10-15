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
            return format_and_return_error(error)

    return inner


def format_and_return_error(error):
    """Format exception and return it as response"""
    status = 400
    message = error.args
    if isinstance(error, MongoErrorHandler):
        status = error.status
        message = error.message
    return jsonify({"message": message}), status


class MongoErrorHandler(Exception):
    """MongoErrorHandler for errors related to mongodb"""
    def __init__(self, message, status):
        Exception.__init__()
        self.message = message
        self.status = status
