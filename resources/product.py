# pylint: disable=no-member

"""CRUD REST-API For Product"""
from http import HTTPStatus
from bson.objectid import ObjectId
from flask import json, Blueprint, request
from flask_restful import Resource, reqparse, abort, Api
from mongoengine import ValidationError
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exception_handler
from util.helper.helper_functions import clean_arguments
from models.Product import Product as product_model
from models.Group import Group as group_model



product_blueprint = Blueprint('product_api', __name__)
api = Api(product_blueprint)


product_args = reqparse.RequestParser()
product_args.add_argument("_id", type=str, help="Problem with Product ID value")
product_args.add_argument("user_id", type=str, help="Problem with User ID value")
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

    # GET - http://127.0.0.1:5000/api/product/<string:product_id>
    @classmethod
    @exception_handler
    def get(cls, product_id):
        """Handles get request for retrieving a single product"""
        product = product_model.objects(_id=product_id).first()
        if len(product) == 0:
            abort(HTTPStatus.NOT_FOUND, message= "Product could not be created")
        return json.loads(product.to_json()), HTTPStatus.CREATED

    # POST - http://127.0.0.1:5000/api/product
    @classmethod
    @exception_handler
    @authenticated
    def post(cls):
        """Handles the post request and creates a new product"""
        body = clean_arguments(product_args)
        product_id = ObjectId()
        new_product = product_model(**body, _id=product_id)
        new_group = group_model(
            product_id=product_id,
            organizer_id=body["user_id"],
            status="Funding"
        )
        try:
            new_product.save()
            new_group.save()

        except ValidationError as validation_error:
            raise MongoErrorHandler(
                validation_error.to_dict(),
                HTTPStatus.BAD_REQUEST
            ) from validation_error
        return json.loads(new_product.to_json()), HTTPStatus.OK

    # PUT - http://127.0.0.1:5000/api/product/<string:product_id>
    @classmethod
    @exception_handler
    @authenticated
    def put(cls, product_id):
        """Handles the put request to update a single product"""
        body = {}
        for key,value in product_args.parse_args().items():
            if value is not None:
                body[key] = value
        try:
            product_model.objects(_id=product_id).first().modify(**body)
        except AttributeError as attr_error:
            raise MongoErrorHandler(
                "Could not find the product",
                HTTPStatus.NOT_FOUND
            ) from attr_error

        return {"message":f"Product with id of {product_id} updated"}, HTTPStatus.OK


    # DELETE - http://127.0.0.1:5000/api/product/<string:product_id>
    @classmethod
    @exception_handler
    @authenticated
    def delete(cls, product_id):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        try:
            group = group_model.objects(product_id=product_id)
            product.delete()
            if len(group) == 0:
                raise MongoErrorHandler(
                    "Product deleted but Group does not exist",
                    HTTPStatus.BAD_REQUEST
                )
            group.delete()
        except Exception as exception:
            raise MongoErrorHandler("Product does not exist", HTTPStatus.BAD_REQUEST) from exception

        return {"message":f"Product with id of {product_id} deleted"}, HTTPStatus.OK


class Products(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    # GET - http://127.0.0.1:5000/api/products
    @classmethod
    @exception_handler
    def get(cls):
        """Handles the get request and returns all the products in the collection"""
        # Handles the search query and pagination
        query = request.args.get("q")
        page_number = request.args.get("page")

        # if no page number is provided then get all the product from the DB
        if page_number is not None:
            # if search query is specified then find product titles that contain that query
            if query is not None:
                # offset helps determine which product object to start with when paginating
                product_limit = 15
                offset = (int(page_number) - 1) * product_limit
                # Objects are filtered by whether the title contains(case-insensitive) the query
                paginated_products = (
                    product_model.objects(title__icontains=query)
                    .skip(offset)
                    .limit(product_limit)
                )
            # if search query is not provided then just paginate all the product objects
            else:
                product_limit = 15
                offset = (int(page_number) - 1) * 15
                paginated_products = product_model.objects.skip(offset).limit(
                    product_limit
                )
            return paginated_products.to_json(), 200
        products = product_model.objects.all()
        return json.loads(products.to_json()), 200


api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_by_id")
api.add_resource(Product, "/api/product", endpoint="product")
api.add_resource(Products, "/api/products")
