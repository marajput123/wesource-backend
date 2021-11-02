""" Main app call """
from http import HTTPStatus
from flask import Flask, json, jsonify
from flask.globals import request
from mongoengine import connect
from flask_restful import Resource, reqparse, abort
from models.User import User
from util.decorators.auth import authenticated, generate_auth_token
from util.decorators.errorHandler import MongoErrorHandler, exception_handler


# Database URL
#MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long
MONGODB_URL = "mongodb+srv://User123:User123@cluster0.dfjru.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
@exception_handler
def index():
    """Index - Mock Route"""
    return jsonify({"hello": "world"})


@app.route("/login", methods=["POST"])
@exception_handler
def login():
    """User login"""
    body = request.get_json()
    user = User.get_by_email(body["email"])
    if user.verify_password(body["password"]):
        return jsonify({"jwt": generate_auth_token(user)})
    return "Username/Password incorrect", HTTPStatus.UNAUTHORIZED


@app.route("/profile", methods=["GET"])
@exception_handler
@authenticated
def profile(**kwargs):
    """Profile page"""
    user = kwargs["current_user"]
    return user.to_json()


@app.route("/register", methods =["POST"])
@exception_handler
def register():
    """Method to register new User"""
    body = request.get_json()
    user = User(firstName = body["firstName"], 
                lastName = body["lastName"], 
                email = body["email"], 
                password = body["password"],
                username = body["username"])
    user.hash_password(body["password"])
    user.save()
    return {"message": "account registered"} , 200
    
@app.route("/user/<string:id>", methods =["DELETE"])
@exception_handler
def delete(id):
    """Method to delete user"""
    user = User.get_by_id(id)
    if not user:
        raise MongoErrorHandler("Id not found", 404)
    else:
        user.delete()
    return {"message": "account deleted"} , 200

@app.route("/user/<username>", methods =["PATCH"])
@exception_handler
def update(username):
    """Method to update user"""
    user = User.get_by_username(username)
    body = request.get_json()
    if not user: 
        raise MongoErrorHandler("Username not found", 404)
    else:
        user.modify(**body)
        user.save()
        return {"message": "accounted updated"} , 200
        