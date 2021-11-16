# pylint: disable=no-member

""" CRUD REST-API Authentication """
from http import HTTPStatus
from flask import json, Blueprint
from flask.globals import request
from flask_restful import Resource, Api, reqparse
from models.User import User
from util.helper.helper_functions import clean_arguments
from util.decorators.auth import authenticated, generate_auth_token
from util.decorators.errorHandler import MongoErrorHandler, exception_handler

authentication_blueprint = Blueprint("authentication_blueprint", __name__)
auth_api = Api(authentication_blueprint)

register_args = reqparse.RequestParser()
user_args = reqparse.RequestParser()

register_args.add_argument("firstName", type=str, help="First name is required")
register_args.add_argument("lastName", type=str, help="lastName name is required")
register_args.add_argument("email", type=str, help="email is required")
register_args.add_argument("username", type=str, help="username is required")
register_args.add_argument("password", type=str, help="password is required")

user_args.add_argument("firstName", type=str, help="First name is required")
user_args.add_argument("lastName", type=str, help="last name is required")


class AuthenticationLogin(Resource):
    """Resource to handle login and accessing user profile"""

    # POST - http://127.0.0.1:5000/api/login
    @staticmethod
    @exception_handler
    def post():
        """POST login"""
        body = request.get_json()
        user = User.get_by_email(body["email"])
        if user.verify_password(body["password"]):
            return {"jwt": generate_auth_token(user)}, HTTPStatus.CREATED
        raise MongoErrorHandler(
            """Email or password are not correct.
            Please make sure you have entered the correct credentials.""",
            400,
        )


class Authentication(Resource):
    """REST Endpoint for accessing/creatin User"""

    # GET - http://127.0.0.1:5000/api/login/<string:user_id>
    @staticmethod
    @exception_handler
    @authenticated
    def get(user_id):
        """GET user info"""
        user = User.objects(_id=user_id)
        return json.loads(user.to_json()), 200

    # POST - http://127.0.0.1:5000/api/auth
    @staticmethod
    @exception_handler
    def post():
        """POST registration"""
        try:
            body = register_args.parse_args()
            user = User(**body)
            user.hash_password(user.password)
            user.save()
            return {"jwt": generate_auth_token(user)}, HTTPStatus.CREATED
        except Exception as exception:
            raise MongoErrorHandler(
                "User could not be created", HTTPStatus.BAD_REQUEST
            ) from exception

    # PUT - http://127.0.0.1:5000/api/auth/<string:user_id>
    @staticmethod
    @exception_handler
    def put(user_id):
        """UPDATE user"""
        try:
            body = clean_arguments(user_args)
            user = User.objects(_id=user_id).modify(**body)
            user.save()
            return {"success": True}, HTTPStatus.CREATED
        except Exception as exception:
            print(exception)
            raise MongoErrorHandler(
                "User could not be updated", HTTPStatus.BAD_REQUEST
            ) from exception


auth_api.add_resource(AuthenticationLogin, "/api/login", endpoint="login_endpoint")
auth_api.add_resource(Authentication, "/api/auth", endpoint="auth_endpoint")
auth_api.add_resource(
    Authentication, "/api/auth/<string:user_id>", endpoint="auth_endpoint_by_id"
)
