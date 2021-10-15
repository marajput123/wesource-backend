"""Item Model"""
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField


class Item(Document):
    """Item collection"""
    _id = ObjectIdField(default=ObjectId())
    title = StringField(max_length=75, required=True)
    description = StringField(max_length=250, required=True)
    price = IntField(min_value=0, required=True)
    quantity = IntField(defualt=1)
    imageURL = StringField()
    productId = ReferenceField("Product")
