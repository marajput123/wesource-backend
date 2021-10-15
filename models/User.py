from bson.objectid import ObjectId
from mongoengine import *
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import EmailField, IntField, StringField

class User(Document):
    _id = ObjectIdField(default=ObjectId())
    firstName = StringField(max_length=50, required=True)
    lastName = StringField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True, unique=True)
    username = StringField(max_length=30, min_length=6, required=True, unique=True)
    password = StringField(max_length=24, min_length=6, required=True)
    rating = IntField(default=0)

