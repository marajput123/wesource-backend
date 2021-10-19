""" Main app call """
from flask import Flask, jsonify
from flask_restful import Api
from util.decorators.errorHandler import exception_handler
from mongoengine import connect
from product import Product, Products

# Have to import models to register in the document registry
import models.User  # pylint: disable=unused-import
import models.Item  # pylint: disable=unused-import
import models.Product  # pylint: disable=unused-import

# Database URL
MONGODB_URL = "mongodb+srv://test2:123@cluster0.fujai.mongodb.net/test"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)
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
