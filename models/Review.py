"""Review Model"""
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import (
    IntField,
    StringField,
)


class Review(Document):
    """User Collection"""

    _id = ObjectIdField(primary_key=True)
    reviewer_id = ObjectIdField(required=True)
    reviewee_id = ObjectIdField(required=True)
    description = StringField(min_value=5, max_length=250, required=True)
    rating = IntField(min_value=1, max_value=5, required=True)
