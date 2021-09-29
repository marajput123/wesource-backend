from flask import Flask, jsonify
from pymongo import MongoClient

# Database URL
MONGODB_URL = 'mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WeSource?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority'

# Database Connection
client = MongoClient(MONGODB_URL, connect=False)

# Databases
testDatabase = client['WeSource']

# Collections

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    dict = {'hello':'world'}
    return jsonify(dict)