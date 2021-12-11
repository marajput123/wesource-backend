# pylint: disable=no-member
# pylint: disable=unused-argument

"""CRUD REST-API For Product"""
from http import HTTPStatus
from datetime import datetime
from flask import json, Blueprint, request
from flask_restful import Api, Resource
from models.Group import Announcement, Group as group_model
from models.Product import Product as product_model
from models.User import User as user_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler


group_blueprint = Blueprint("group_api", __name__)
api = Api(group_blueprint)


class Group(Resource):
    """CRUD endpoints for Group"""

    # GET - http://127.0.0.1:5000/api/group/<string:group_id>
    @classmethod
    @exception_handler
    def get(cls, group_id):  # pylint: disable-msg=too-many-locals
        """A get request that returns the entire populated group object"""
        group = group_model.get_by_id(group_id)
        user_ids = group["user_id"]
        group = json.loads(group.to_json())

        # Fields or rather keys to remove from the user dictionary
        remove_fields = ["rating", "productId", "reviewId"]

        # Format datetime object to a string
        for announcements in group["announcement"]:
            # Return date e.g. December 07,2021
            timestamp = announcements["date"]["$date"]
            # timestamp is in millisecond and must divide by 1000 to convert to secs
            date = cls._convert_to_date(timestamp)
            announcements["date"] = date

        # Populate the product_id with the object
        product_id = group["Product"]["$oid"]
        product = json.loads(product_model.objects(_id=product_id).first().to_json())
        # Return date e.g. December 07,2021
        timestamp = product["date"]["$date"]
        date = cls._convert_to_date(timestamp)
        product["date"] = date
        group["Product"] = product

        # Populate the organizer_id with the object
        # Only the _id, username, and imageURL field will be retrieved
        # but for some reason the other fields will be included though they'll be empty
        # and will be removed after the query
        organizer_id = group["Organizer"]["$oid"]
        organizer = json.loads(
            user_model.objects(_id=organizer_id)
            .fields(_id=1, username=1, imageURL=1)
            .first()
            .to_json()
        )
        for field in remove_fields:
            del organizer[field]
        group["Organizer"] = organizer

        # Populate the user_id with the object
        # Only the _id, username, and imageURL field will be retrieved
        # but for some reason the other fields will be included though they'll be empty
        # and will be removed after the query
        users = (
            user_model.objects().fields(_id=1, username=1, imageURL=1).in_bulk(user_ids)
        )

        users_list = []
        for uid in users:
            user = json.loads(users[uid].to_json())
            for field in remove_fields:
                del user[field]
            users_list.append(user)
        group["user_id"] = users_list

        return group, HTTPStatus.OK

    @classmethod
    def _convert_to_date(cls, timestamp):
        date = datetime.fromtimestamp(timestamp / 1000).strftime("%B %d,%Y")
        return date

    # POST - http://127.0.0.1:5000/api/group/<string:group_id>
    @classmethod
    @exception_handler
    @authenticated
    def post(cls, group_id, current_user=None):
        """Add user to the group"""
        try:
            body = request.get_json()
            group = group_model.get_by_id(group_id)
            print(body)
            group["user_id"].append(body["user_id"])
            group.save()
            return json.loads(group.to_json()), HTTPStatus.CREATED
        except Exception as exception:
            print(exception)


    # PUT - http://127.0.0.1:5000/api/group/<string:group_id>
    @classmethod
    @exception_handler
    @authenticated
    def put(cls, group_id, current_user=None):
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


class GroupQuery(Resource):
    """CRUD for quering groups"""

    # GET - http://127.0.0.1:5000/api/group/<params>
    @classmethod
    @exception_handler
    def get(cls):
        """GET groups that the user has joined"""
        groups = group_model.objects(user_id=request.args["user_id"])
        product_ids = []
        for group in groups:
            product_ids.append(str(group.product_id))
        return {"product_ids": product_ids}, HTTPStatus.OK


class GroupAnnouncement(Resource):
    """CURD for announcements"""

    # POST http://127.0.0.1:5000/api/group/announcement/<string:group_id>
    @classmethod
    @exception_handler
    @authenticated
    def post(cls, group_id ,current_user=None):
        """POST announcement to the group"""
        try:
            body = request.get_json()
            group = group_model.objects(_id=group_id)[0]
            announcement = Announcement(description=body["description"])
            group["announcement"].append(announcement)
            group.save()
            return json.loads(announcement.to_json()), HTTPStatus.CREATED
        except Exception:
            return {"message":"failed"}, HTTPStatus.BAD_REQUEST

    # DELETE http://127.0.0.1:5000/api/group/announcement/<string:group_id>
    @classmethod
    @exception_handler
    @authenticated
    def delete(cls, group_id ,current_user=None):
        """DELETE announcement from the group"""
        try:
            body = request.get_json()
            print(body)
            group = group_model.objects(_id=group_id)[0]
            announcement_id = body["announcementId"]
            new_list = []
            for announcement in group["announcement"]:
                if str(announcement._id) != str(announcement_id):
                    new_list.append(announcement)
            group["announcement"] = new_list
            group.save()
            return {"message":"delete"}, HTTPStatus.OK
        except Exception as e:
            print(e)
            return {"message":"failed"}, HTTPStatus.BAD_REQUEST

    @classmethod
    def _convert_to_date(cls, timestamp):
        date = datetime.fromtimestamp(timestamp / 1000).strftime("%B %d,%Y")
        return date
        

api.add_resource(Group, "/api/group/<string:group_id>", endpoint="group_by_id")
api.add_resource(GroupQuery, "/api/group", endpoint="group")
api.add_resource(GroupAnnouncement, "/api/group/announcement/<string:group_id>", endpoint="announcements")
api.add_resource(GroupLanding, "/api/group/landing", endpoint="group_landing")
