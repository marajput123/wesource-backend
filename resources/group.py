# pylint: disable=no-member

"""CRUD REST-API For Product"""
from http import HTTPStatus
from flask import json, Blueprint, request
from flask_restful import Api, Resource, reqparse
from models.Group import Group as group_model
from models.Product import Product as product_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler


group_blueprint = Blueprint("group_api", __name__)
api = Api(group_blueprint)

group_args = reqparse.RequestParser()
group_args.add_argument(
    "product_id", type=str, help="Problem with Product Id validation"
)
group_args.add_argument(
    "organizer_id", type=str, help="Problem with Organizer Id value"
)
group_args.add_argument(
    "user_ids",
    type=list,
    help="Problem with the list of the user ids' value",
    action="append",
)
group_args.add_argument("status", type=int, help="Problem with status value")


class Group(Resource):
    """CRUD endpoints for Groups"""

    # GET - http://127.0.0.1:5000/api/group/<string:group_id>
    @classmethod
    @exception_handler
    def get(cls, group_id):
        """Get Group"""
        group = group_model.get_by_id(group_id)
        return json.loads(group.to_json()), HTTPStatus.OK

    # POST - http://127.0.0.1:5000/api/group/<string:group_id>
    @classmethod
    @exception_handler
    @authenticated
    def post(cls, group_id):
        """Add user to the group"""
        body = request.get_json()
        group = group_model.get_by_id(group_id)
        group["user_ids"].append(body["user_id"])
        group.save()
        return json.loads(group.to_json()), HTTPStatus.CREATED

    @classmethod
    @exception_handler
    @authenticated
    def put(cls, group_id):
        """Update group"""
        body = request.get_json()
        group = group_model.get_by_id(group_id).first().modify(**body)
        group.save()


class GroupLanding(Resource):
    """CRUD for displaying delivered products for the landing page"""

    # GET - http://127.0.0.1:5000/api/group/landing
    @classmethod
    @exception_handler
    def get(cls):

        """Handles the get request and returns the number of products specified for the landing page"""

        # Takes in an arg of num, the number of delivered product to query for
        num_delivered = request.args.get("num", 3, type=int)
        if num_delivered <= 0:
            # Does not currently check upperlimit so db size
            return "Invalid product quantity", HTTPStatus.BAD_REQUEST

        # Gets the set quantity of random document from the db where
        # status == "Delivered" and only the product_id field is projected
        groups = group_model.objects.aggregate(
            {"$match": {"status": "Delivered"}},
            {"$sample": {"size": num_delivered}},
            {"$project": {"_id": 0, "product_id": "$product_id"}},
        )
        product_id = []
        for product in groups:
            product_id.append(product["product_id"])
        products = product_model.objects(_id__in=product_id)
        return json.loads(products.to_json()), HTTPStatus.OK


api.add_resource(Group, "/api/group/<string:group_id>", endpoint="group_by_id")
api.add_resource(Group, "/api/group", endpoint="group")
api.add_resource(GroupLanding, "/api/group/landing", endpoint="group_landing")