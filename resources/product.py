# pylint: disable=no-member
# pylint: disable=unused-argument

"""CRUD REST-API For Product"""
from http import HTTPStatus
from bson import json_util
from bson.objectid import ObjectId
from flask import json, Blueprint, request
from flask_restful import Resource, reqparse, Api
from mongoengine import ValidationError
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exception_handler
from util.helper.helper_functions import clean_arguments, clean_product_queries
from models.Product import Product as product_model
from models.Group import Group as group_model


product_blueprint = Blueprint("product_api", __name__)
api = Api(product_blueprint)


product_args = reqparse.RequestParser()
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
    "imageURL", type=str, help="Problem with ImageURL value"
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
        if not product:
            raise MongoErrorHandler("Product could not be found", HTTPStatus.NOT_FOUND)
        return json.loads(product.to_json()), HTTPStatus.ACCEPTED

    # POST - http://127.0.0.1:5000/api/product
    @classmethod
    @exception_handler
    @authenticated
    def post(cls, current_user=None):
        """Handles the post request and creates a new product"""
        body = clean_arguments(product_args)
        group_id = ObjectId()
        product_id = ObjectId()
        body["organizer_username"] = current_user.username
        body["status"] = "Funding"
        body["group_id"] = group_id
        new_product = product_model(**body, _id=product_id)
        new_group = group_model(
            product_id=product_id,
            organizer_id=current_user._id,
            user_id=[current_user._id],
            _id=group_id
        )
        try:
            new_product.save()
            new_group.save()

        except ValidationError as validation_error:
            print(validation_error)
            raise MongoErrorHandler(
                validation_error.to_dict(), HTTPStatus.BAD_REQUEST
            ) from validation_error
        return json.loads(new_product.to_json()), HTTPStatus.OK

    # PUT - http://127.0.0.1:5000/api/product/<string:product_id>
    @classmethod
    @exception_handler
    @authenticated
    def put(cls, product_id, current_user=None):
        """Handles the put request to update a single product"""
        body = clean_arguments(product_args)
        try:
            product_model.objects(_id=product_id).first().modify(**body)
        except AttributeError as attr_error:
            raise MongoErrorHandler(
                "Could not find the product", HTTPStatus.NOT_FOUND
            ) from attr_error

        return {"message": f"Product with id of {product_id} updated"}, HTTPStatus.OK

    # DELETE - http://127.0.0.1:5000/api/product/<string:product_id>
    @classmethod
    @exception_handler
    @authenticated
    def delete(cls, product_id, current_user):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        group = group_model.objects(product_id=product_id)
        if len(product) == 0:
            raise MongoErrorHandler("Product does not exist", HTTPStatus.BAD_REQUEST)
        if len(group) == 0:
            raise MongoErrorHandler("Group does not exist", HTTPStatus.BAD_REQUEST)
        product.delete()
        group.delete()
        return {"message": f"Product with id of {product_id} deleted"}, HTTPStatus.OK


class Products(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    # GET - http://127.0.0.1:5000/api/products
    @classmethod
    @exception_handler
    def get(cls):
        """Handles the get request and returns all the products in the collection"""
        # Handles the search query and pagination
        # query = request.args.get("q")
        page_number = request.args.get("page")
        query = clean_product_queries(request)
        product_count = len(product_model.objects(**query))
        # if no page number is provided then get all the product from the DB
        if page_number is not None:
            # if search query is specified then find product titles that contain that query
            if len(query) != 0:
                # offset helps determine which product object to start with when paginating
                product_limit = 15
                offset = (int(page_number) - 1) * product_limit
                # Objects are filtered by whether the title contains(case-insensitive) the query
                paginated_products = (
                    product_model.objects(**query).skip(offset).limit(product_limit)
                )
                product_count = len(product_model.objects(**query))

            # if search query is not provided then just paginate all the product objects
            else:
                product_limit = 15
                offset = (int(page_number) - 1) * 15
                paginated_products = product_model.objects.skip(offset).limit(
                    product_limit
                )
                product_count = len(product_model.objects(**query))
            json_response = {
                "data": json.loads(paginated_products.to_json()),
                "total_count": product_count,
            }
            return json_response, HTTPStatus.ACCEPTED
        products = product_model.objects(**query)
        json_response = {
            "data": json.loads(products.to_json()),
            "total_count": product_count,
        }
        return json_response, HTTPStatus.OK


class UserProduct(Resource):
    """CRUD for displaying all of the user's joined groups"""

    # GET - http://127.0.0.1:5000/api/user/<string:user_id>/joined-groups
    @classmethod
    @exception_handler
    @authenticated
    def get(cls, user_id, current_user=None):
        """GET method that uses the Product collection rather than Group"""

        # user_id is not used but will just be checked
        if user_id != str(current_user["_id"]):
            return {
                "message": "User is not allowed to get other user's joined groups"
            }, HTTPStatus.UNAUTHORIZED

        # Get the user's productId list after being authenticated and page number
        user_groups = current_user["productId"]
        page_number = request.args.get("page")

        # If no page number is provided default to page 1
        if page_number is None:
            page_number = 1

        # offset helps determine which product object to start with when paginating
        group_limit = 15
        offset = (int(page_number) - 1) * group_limit

        # Products are filtered by whether the id is in the user['productId']
        # The filtered product are ordered in decending order by the _id
        # Assume that the most recent _id are displayed(most recent group joined)
        paginated_groups = (
            product_model.objects.filter(_id__in=user_groups)
            .skip(offset)
            .limit(group_limit)
            .order_by("-_id")
        )
        group_count = len(paginated_groups)
        json_response = {
            "data": json.loads(paginated_groups.to_json()),
            "total_count": group_count,
        }
        return json_response, HTTPStatus.ACCEPTED


class ProductsLanding(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    # GET - http://127.0.0.1:5000/api/products/landing
    @classmethod
    @exception_handler
    def get(cls):
        """A get request that returns the number of specified product for the landing page"""
        num_product = request.args.get("num", 3, type=int)
        if num_product <= 0:
            # Does not currently check upperlimit so db size
            return "Invalid product quantity", HTTPStatus.BAD_REQUEST

        # Gets the set quantity of random document from the db
        products = product_model.objects.aggregate({"$sample": {"size": num_product}})
        return json.loads(json_util.dumps(products)), HTTPStatus.OK


api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_by_id")
api.add_resource(Product, "/api/product", endpoint="product")
api.add_resource(Products, "/api/products", endpoint="products")
api.add_resource(
    UserProduct, "/api/user/<string:user_id>/joined-groups", endpoint="joined_groups"
)
api.add_resource(ProductsLanding, "/api/products/landing", endpoint="product_landing")
