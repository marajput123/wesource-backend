from flask.json import jsonify


def exceptionHandler(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return formatAndReturnError(e)
    return inner


def formatAndReturnError(e):
    status = 400
    message = e.args
    if isinstance(e, MongoErrorHandler):
        status = e.status
        message = e.message
    return jsonify({"message":message}),status



class MongoErrorHandler(Exception):
    def __init__(self, message, status):
        super()
        self.message = message
        self.status = status