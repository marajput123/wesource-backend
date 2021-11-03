# pylint: disable=no-member

"""CRUD REST-API For Product"""
from http import HTTPStatus
from flask import json, Blueprint, request
from flask_restful import Resource, reqparse, abort, Api
from mongoengine import ValidationError
from models.Product import Product as product_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exception_handler


product_blueprint = Blueprint("product_api", __name__)
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

    @staticmethod
    def get(product_id):
        """Handles get request for retrieving a single product"""
        product = product_model.objects(_id=product_id).first()
        if len(product) == 0:
            abort(HTTPStatus.NOT_FOUND, message="Product could not be created")
        return json.loads(product.to_json()), HTTPStatus.CREATED

    @staticmethod
    @exception_handler
    @authenticated
    def post():
        """Handles the post request and creates a new product"""
        product = product_args.parse_args()
        new_product = product_model(**product)
        try:
            new_product.save()
        except ValidationError as validation_error:
            raise MongoErrorHandler(
                ValidationError.to_dict(), #pylint: disable = no-value-for-parameter
                HTTPStatus.BAD_REQUEST) from validation_error
        return json.loads(new_product.to_json()), HTTPStatus.OK

    @staticmethod
    # @exception_handler
    # @authenticated
    def put(product_id):
        """Handles the put request to update a single product"""
        body = {}
        for key, value in product_args.parse_args().items():
            if value is not None:
                body[key] = value
        try:
            product_model.objects(_id=product_id).first().modify(**body)
        except AttributeError as attr_err:
            raise MongoErrorHandler(
                "Could not update the product",
                HTTPStatus.NOT_FOUND) from attr_err
        return {"message": f"Product with id of {product_id} updated"}, HTTPStatus.OK

    @staticmethod
    @exception_handler
    @authenticated
    def delete(product_id):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        # If product can't be found then abort
        if len(product) == 0:
            abort(HTTPStatus.BAD_REQUEST, message="Can not delete product")
        else:
            product.delete()
        return {"message": f"Product with id of {product_id} deleted"}, HTTPStatus.OK


class Products(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    @staticmethod
    def get():
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
