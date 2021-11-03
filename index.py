""" Main app call """
from flask import Flask
from mongoengine import connect
from flask_cors import CORS

from resources.product import product_blueprint
from resources.authentication import authentication_blueprint

# Have to import models to register in the document registry
import models.User  # pylint: disable=unused-import
import models.Product  # pylint: disable=unused-import

# Database URL
MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long

# Database Connection
connect(host=MONGODB_URL)


app = Flask(__name__)
CORS(app)


app.register_blueprint(product_blueprint)
app.register_blueprint(authentication_blueprint)


