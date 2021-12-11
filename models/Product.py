"""Product Model"""
from datetime import datetime
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import (
    IntField,
    EmbeddedDocumentListField,
    EmbeddedDocument,
    StringField,
    DecimalField,
    DateTimeField,
)


class Item(EmbeddedDocument):
    """Item Schema"""

    _id = ObjectIdField(default=ObjectId, primary_key=True)
    title = StringField(max_length=75, required=True)
    description = StringField(max_length=250, required=True)
    price = DecimalField(min_value=0, required=True)
    quantity = IntField(default=1)
    imageURL = StringField()


class Product(Document):
    """Product Schema"""

    _id = ObjectIdField(default=ObjectId, primary_key=True)
    title = StringField(max_length=75, required=True)
    description = StringField(max_length=250, required=True)
    price = DecimalField(min_value=0, precision=2, required=True)
    quantity = IntField(default=1)
    imageURL = StringField()
    date = DateTimeField(default=datetime.utcnow)
    status = StringField(required=True)
    organizer_username = StringField(db_field="Organizer", required=True)
    group_id = ObjectIdField(db_field="Group", required=True)
    items = EmbeddedDocumentListField("Item")
