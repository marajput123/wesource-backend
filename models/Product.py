"""Product Model"""
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import (
    IntField,
    ListField,
    ReferenceField,
    StringField,
    DecimalField,
)


class Product(Document):
    """Product Collection"""

    _id = ObjectIdField(default=ObjectId())
    title = StringField(max_length=75, required=True)
    description = StringField(max_length=250, required=True)
    price = DecimalField(min_value=0, precision=2, required=True)
    quantity = IntField(default=1, required=True)
    imageURL = StringField()
    itemIds = ListField(ReferenceField("Item"), default=[])
