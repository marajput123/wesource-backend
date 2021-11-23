# pylint: disable=no-member
# pylint: disable=unused-argument

"""CRUD REST-API For Product"""
from http import HTTPStatus
from bson import json_util
from flask import json, Blueprint, request
from flask_restful import Api, Resource
from models.Group import Group as group_model
from models.Product import Product as product_model
from models.User import User as user_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler
from util.helper.helper_functions import clean_arguments, clean_product_queries


group_blueprint = Blueprint("group_api", __name__)
api = Api(group_blueprint)


class Group(Resource):
    """CRUD endpoints for Group"""

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
    def post(cls, group_id, current_user):
        """Add user to the group"""
        body = request.get_json()
        group = group_model.get_by_id(group_id)
        group["user_ids"].append(body["user_id"])
        group.save()
        return json.loads(group.to_json()), HTTPStatus.CREATED

    @classmethod
    @exception_handler
    @authenticated
    def put(cls, group_id, current_user):
        """Update group"""
        body = request.get_json()
        group = group_model.get_by_id(group_id).first().modify(**body)
        group.save()


class Groups(Resource):
    """CRUD endpoints for Groups"""

    # GET - http://127.0.0.1:5000/api/groups
    @classmethod
    # @exception_handler
    def get(cls):
        """Handles the get request and returns all the products in the collection"""
        # Handles the search query and pagination
        # query = request.args.get("q")
        page_number = request.args.get("page")
        query = clean_product_queries(request)

        # if no page number is provided then get all the product from the DB
        if page_number is not None:
            # if search query is specified then find product titles that contain that query
            if len(query) != 0:
                # offset helps determine which product object to start with when paginating
                product_limit = 15
                offset = (int(page_number) - 1) * product_limit
                # Since it only queries product, the dates querying wont work
                paginated_products = (
                    product_model.objects(**query)
                    .skip(offset)
                    .limit(product_limit)
                    .fields(_id=1)
                )
                # Get a list of string from the objectIds
                product_ids = []
                for id in paginated_products:
                    product_ids.append(str(id["_id"]))

                # Filter groups that have a product_id in the product_ids' list
                groups = group_model.objects.filter(product_id__in=product_ids)

                groups_dict = json.loads(groups.to_json())
                for group in groups_dict:
                    group["Product"] = json.loads(
                        product_model.objects(_id=group["Product"]["$oid"])
                        .first()
                        .to_json()
                    )
                    group["Organizer"] = json.loads(
                        user_model.objects(_id=group["Organizer"]["$oid"])
                        .first()
                        .to_json()
                    )

                group_count = len(groups_dict)

            # if search query is not provided then just paginate all the product objects
            else:
                group_limit = 15
                offset = (int(page_number) - 1) * 15
                paginated_groups = group_model.objects.skip(offset).limit(group_limit)
                group_count = len(paginated_groups)

                groups_dict = json.loads(paginated_groups.to_json())
                print(groups_dict)
                for group in groups_dict:
                    group["Product"] = json.loads(
                        product_model.objects(_id=group["Product"]["$oid"])
                        .first()
                        .to_json()
                    )
                    group["Organizer"] = json.loads(
                        user_model.objects(_id=group["Organizer"]["$oid"])
                        .first()
                        .to_json()
                    )

            json_response = {
                "data": groups_dict,
                "total_count": group_count,
            }
            return json_response, HTTPStatus.ACCEPTED
        # Method 1: set the field to the object but it removes the field itself so no go
        # groups = group_model.objects.all()
        # for group in groups:
        #     group["product_id"] = product_model.objects(_id=group["product_id"]).first()

        groups = group_model.objects.all()
        groups_dict = json.loads(groups.to_json())

        for group in groups_dict:
            group["Product"] = json.loads(
                product_model.objects(_id=group["Product"]["$oid"]).first().to_json()
            )
            group["Organizer"] = json.loads(
                user_model.objects(_id=group["Organizer"]["$oid"]).first().to_json()
            )
        group_count = len(groups_dict)

        # Method 2: use aggregation and $lookup to populate the field but instead it returns an empty list no go
        # pipeline = [
        #     {
        #         "$lookup": {
        #             "from": "product",
        #             "localField": "product_id",
        #             "foreignField": "_id",
        #             "as": "product_id",
        #         }
        #     }
        # ]
        # groups = group_model.objects.all().aggregate(pipeline)
        json_response = {
            "data": groups_dict,
            "total_count": group_count,
        }
        return json_response, HTTPStatus.OK


class GroupLanding(Resource):
    """CRUD for displaying delivered products for the landing page"""

    # GET - http://127.0.0.1:5000/api/group/landing
    @classmethod
    @exception_handler
    def get(cls):

        """A get request that returns the number of specified product for the landing page"""

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
api.add_resource(Groups, "/api/groups", endpoint="groups")
api.add_resource(GroupLanding, "/api/group/landing", endpoint="group_landing")
