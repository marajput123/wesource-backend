from flask import json, jsonify, Blueprint
from flask.globals import request
from flask_restful import Resource, Api

from models.User import User
from util.decorators.auth import authenticated, generate_auth_token
from util.decorators.errorHandler import MongoErrorHandler, exception_handler

authentication_blueprint = Blueprint("authentication_blueprint", __name__)
auth_api = Api(authentication_blueprint)

class Authentication(Resource):
    @exception_handler
    def post(self):
        """User login"""
        body = request.get_json()
        user = User.get_by_email(body["email"])
        if user.verify_password(body["password"]):
            return jsonify({"jwt": generate_auth_token(user)})
        raise MongoErrorHandler("Email or password are not correct. Please make sure you have entered the correct credentials.", 400)
        
    @exception_handler
    @authenticated
    def get(self, user_id):
        """Profile page"""
        user = User.objects(_id = user_id)
        return json.loads(user.to_json())
    
auth_api.add_resource(Authentication, "/api/login", endpoint="auth_endpoint")
auth_api.add_resource(Authentication, "/api/login/<string:user_id>", endpoint="auth_endpoint_by_id")
