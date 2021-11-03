# pylint: disable=no-member

"""CRUD REST-API For Product"""
from flask import json, Blueprint
from flask_restful import Resource, reqparse, abort, Api, Resource
from mongoengine import ValidationError
from models.Product import Product as product_model
from http import HTTPStatus
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler


product_blueprint = Blueprint('product_api', __name__)
api = Api(product_blueprint)


product_args = reqparse.RequestParser()
product_args.add_argument("_id", type=str, help="Problem with Product ID value")
product_args.add_argument(
    "title", type=str, help="Problem with Product Name validation"
)
product_args.add_argument(
    "description", type=str, help="Problem with Product Description value"
)
product_args.add_argument("price", type=float, help="Problem with Product Price value")
product_args.add_argument(
    "quantity", type=int, help="Problem with Product Quantity value"
)
product_args.add_argument(
    "imageURL", type=str, help="Problem with Product Image URL value"
)
product_args.add_argument(
    "items",
    type=dict,
    help="Problem with the list of the items' value",
    action="append",
)


class Product(Resource):
    """CRUD for accessing/manipulating a single product document"""

    def get(self,product_id):
        """Handles get request for retrieving a single product"""
        product = product_model.objects(_id=product_id).first()
        if len(product) == 0:
            abort(HTTPStatus.NOT_FOUND, message= "Product could not be created")
        return json.loads(product.to_json()), HTTPStatus.CREATED

    # @exception_handler
    # @authenticated
    def post(self):
        """Handles the post request and creates a new product"""
        product = product_args.parse_args()
        new_product = product_model(**product)
        try:
            new_product.save()
        except ValidationError:
            abort(HTTPStatus.BAD_REQUEST, message=ValidationError.to_dict())
        return json.loads(new_product.to_json()), HTTPStatus.OK

    # @exception_handler
    # @authenticated
    def put(self, product_id):
        """Handles the put request to update a single product"""
        body = {}
        for key,value in product_args.parse_args().items():
            if value != None:
                body[key] = value
        try:
            product_model.objects(_id=product_id).first().modify(**body)
        except Exception as e:
            abort(HTTPStatus.NOT_FOUND, message="Could not find the product")
        return {"message":f"Product with id of {product_id} updated"}, HTTPStatus.OK
    
    # @exception_handler
    # @authenticated
    def delete(self, product_id):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        # If product can't be found then abort
        if len(product) == 0:
            abort(HTTPStatus.BAD_REQUEST, message="Can not delete product")
        else:
            product.delete()
        return {"message":f"Product with id of {product_id} deleted"}, HTTPStatus.OK


class Products(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    def get(self):
        """Handles the get request and returns all the products in the collection"""
        products = product_model.objects.all()
        return json.loads(products.to_json()), HTTPStatus.OK


api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_by_id")
api.add_resource(Product, "/api/product", endpoint="product")
api.add_resource(Products, "/api/products")