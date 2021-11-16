"""CRUD REST-API For Product"""
from http import HTTPStatus
from flask import json, Blueprint, request
from flask_restful import Api, Resource
from models.Group import Group as group_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler

group_blueprint = Blueprint("group_api", __name__)
api = Api(group_blueprint)


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


api.add_resource(Group, "/api/group/<string:group_id>", endpoint="group_by_id")
api.add_resource(Group, "/api/group", endpoint="group")
