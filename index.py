""" Main app call """
from flask import Flask, jsonify
from mongoengine import connect
from bson.objectid import ObjectId
from models.Product import Product
from models.Item import Item
from models.User import User
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exceptionHandler 


# Database URL
MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
@exceptionHandler
def index():
    return jsonify({"hello":"world"})

