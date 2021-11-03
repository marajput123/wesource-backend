"""User Model"""
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import EmailField, IntField, ListField, ReferenceField, StringField
from werkzeug.security import generate_password_hash, check_password_hash


from util.decorators.errorHandler import MongoErrorHandler


# pylint: disable=no-member
class Group(Document):
    """Group Collection"""
    
    _id = ObjectIdField(default=ObjectId(), primary_key=True)
    product_id = ObjectIdField(db_field="Product", required=True)
    organizer_id = ObjectIdField(db_field="User", required=True)
    user_ids = ListField(ObjectIdField(db_field="User", required=True))
    status = StringField(required=True)

    @classmethod
    def get_by_id(cls, group_id):
        group = Group.objects(_id=group_id).first()
        return group