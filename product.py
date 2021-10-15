from flask import request, jsonify, Blueprint, abort
from pymongo import ReturnDocument
from db import productCollection
from bson import json_util
from bson.objectid import ObjectId
# import json

product_api = Blueprint('product', __name__)


@product_api.route('/api/product/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    # GET request
    if request.method == 'GET':
        product = productCollection.find_one({'_id': ObjectId(product_id)})
        if product is None:
            abort(404)
        # Turn ObjectId into a string when returning json data
        product['_id'] = str(product['_id'])
        # json_util.dumps is used to serialize mongodb's ObjectId
        # then the use of json.loads to deserialize into python dictionary
        # jsonify would just serialize the data to a JSON
        return jsonify(product), 200
    # PUT request which updates the product
    elif request.method == 'PUT':
        updatedProduct = request.form.to_dict()
        # filter/find by _id field must be an ObjectId else the product_id string will replace ObjectId
        product = productCollection.find_one_and_update({'_id': ObjectId(product_id)},
                                                        {'$set': {'age': updatedProduct['age'],
                                                                  'name': updatedProduct['name'],
                                                                  'race': updatedProduct['race']}},
                                                        upsert=True,
                                                        return_document=ReturnDocument.AFTER)
        if product is None:
            abort(404)
        return jsonify(updatedProduct), 200
    # DELETE request
    else:
        removedProduct = productCollection.find_one_and_delete(
            {'_id': ObjectId(product_id)})
        if removedProduct is None:
            abort(404)
        removedProduct['_id'] = str(removedProduct['_id'])
        return jsonify(removedProduct), 202


@product_api.route('/api/product', methods=['POST'])
def addProduct():
    # If flat is True the returned dict will only have the first item present, if flat is False all values will be returned as lists.
    product = productCollection.insert_one(request.form.to_dict(flat=True))
    # Access pymongo.results.InsertOneResult object using the inserted_id
    addedProduct = productCollection.find_one({'_id': product.inserted_id})
    addedProduct['_id'] = str(addedProduct['_id'])
    print(addedProduct)
    return jsonify(addedProduct), 202


@product_api.route('/api/products', methods=['GET'])
def getProducts():
    products = productCollection.find()
    if products is None:
        abort(404)
    return jsonify(json_util.dumps(products)), 200
