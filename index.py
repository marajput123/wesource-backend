""" Main app call """
from http import HTTPStatus
from flask import Flask, jsonify
from flask.globals import request
from flask_restful import Api
from mongoengine import connect
from flask_cors import CORS, cross_origin

from models.User import User
from util.decorators.auth import authenticated, generate_auth_token
from util.decorators.errorHandler import MongoErrorHandler, exception_handler
from product import Product, Products

# Have to import models to register in the document registry
import models.User  # pylint: disable=unused-import
import models.Product  # pylint: disable=unused-import

# Database URL
MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)
CORS(app)
api = Api(app)

# Product routes
api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_by_id")
api.add_resource(Product, "/api/product", endpoint="product")
api.add_resource(Products, "/api/products")


@app.route("/", methods=["POST", "GET"])
@exception_handler
def index():
    """Index - Mock Route"""
    return jsonify({"hello": "world"})


@app.route("/api/login", methods=["POST"])
@exception_handler
def login():
    """User login"""
    body = request.get_json()
    user = User.get_by_email(body["email"])
    if user.verify_password(body["password"]):
        return jsonify({"jwt": generate_auth_token(user)})
    raise MongoErrorHandler("Email or password! are not correct. Please make sure you have entered the correct credentials.", 400)
    


@app.route("/profile", methods=["GET"])
@exception_handler
@authenticated
def profile(**kwargs):
    """Profile page"""
    user = kwargs["current_user"]
    return user.to_json()


@app.route("/user/<id>", methods=["DELETE"])
@exception_handler
def user(id):
    print(id)
    user  = User.get_by_id(id)
    print(user.firstName)
    return {"message":"found"}, 200
