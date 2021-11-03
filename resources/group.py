"""CRUD REST-API For Product"""
from flask import json, Blueprint, request 
from flask_restful import Resource, reqparse, abort, Api, Resource
from mongoengine import ValidationError
from models.Group import Group as group_model
from http import HTTPStatus
from util.decorators.auth import authenticated
from util.decorators.errorHandler import exception_handler

group_blueprint = Blueprint("group_api", __name__)
api = Api(group_blueprint)

class Group(Resource):
    # GET - http://127.0.0.1:5000/api/group/<string:group_id>
    @exception_handler
    def get(self, group_id):
        """Get Group"""
        group = group_model.get_by_id(group_id)
        return json.loads(group.to_json()), 200

    # POST - http://127.0.0.1:5000/api/group/<string:group_id>
    @exception_handler
    @authenticated
    def post(self, group_id):
        """Add user to the group"""
        body = request.get_json()
        group = group_model.get_by_id(group_id)
        group["user_ids"].append(body["user_id"])
        group.save()
        return json.loads(group.to_json()), 202



api.add_resource(Group, "/api/group/<string:group_id>", endpoint="group_by_id")
api.add_resource(Group, "/api/group", endpoint="group")
