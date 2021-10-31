""" Main app call """
from http import HTTPStatus
from flask import Flask, json, jsonify
from flask.globals import request
from mongoengine import connect
from flask_restful import Resource, reqparse, abort
from models.User import User
from util.decorators.auth import authenticated, generate_auth_token
from util.decorators.errorHandler import exception_handler


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
    "Method to register new User"
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    username = body["username"]
    firstname = body["firstname"]
    lastname = body["lastname"]
    user = User(firstName = firstname, 
    lastName = lastname, 
    email = email, 
    password = password,
    username = username)
    user.hash_password()
    user.save()

user_args = request.RequestParser()
user_args.add_arguement("_id", type=str, help = "Id of User")
user_args.add_arguement("email", type=str, help = "User Email")
user_args.add_arguement("firstname", type=str, help = "User firstname")
user_args.add_arguement("lastname", type=str, help = "User lastname")
user_args.add_arguement("username", type=str, help = "User username")
user_args.add_arguement("password", type=str, help = "User password")

class User(Resource):

    "Method to delete user"
    @staticmethod
    def delete(user_id):
        user = user_id.objects(_id=user_id)
        if not user:   
            return jsonify({"Error" : "ID not found"})
        else:
            user.delete()
        return 204, "User successfully deleted"

    "Method to update user"
    @staticmethod
    def patch(user_id):
        body = request.json()
        user = User.get_by_id(body["id"])
        result = user(_id = user_id).update_one(
            username = user.username,
            email = user.email,
            firstname = user.firstname,
            lastname = user.lastname
        )
        if not result:
            return 404, "User ID not found"
        else:
            return 200, "User succesfully updated"