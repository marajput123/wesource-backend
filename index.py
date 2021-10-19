""" Main app call """
from flask import Flask, jsonify
from mongoengine import connect
from util.decorators.errorHandler import exception_handler

# Needed to run flask app with flask_restful
import flask.scaffold

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
# from product import product_api
from flask_restful import Resource, Api
from product import Product, Products

# Have to import models
import models.User
import models.Item
import models.Product


# Database URL
MONGODB_URL = "mongodb+srv://test2:123@cluster0.fujai.mongodb.net/test"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)
api = Api(app)
api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_by_id")
api.add_resource(Product, "/api/product", endpoint="product")
api.add_resource(Products, "/api/products")


@app.route("/", methods=["POST", "GET"])
@exception_handler
def index():
    """Index - Mock Route"""
    return jsonify({"hello": "world"})
