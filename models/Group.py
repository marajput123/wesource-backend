"""Group Model"""
from datetime import datetime
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import (
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
    DateField,
)

# pylint: disable=no-member
class Announcement(EmbeddedDocument):
    """Announcement Schema"""

    _id = ObjectIdField(default=ObjectId, primary_key=True)
    description = StringField(max_length=250, required=True)
    date = DateField(default=datetime.utcnow)


class Group(Document):
    """Group Collection"""

    _id = ObjectIdField(default=ObjectId, primary_key=True)
    product_id = ObjectIdField(db_field="Product", required=True)
    organizer_id = ObjectIdField(db_field="Organizer", required=True)
    user_id = ListField(ObjectIdField(db_field="User", required=True))
    announcement = EmbeddedDocumentListField(Announcement)

    @classmethod
    def get_by_id(cls, group_id):
        """Get Group by ID"""
        group = Group.objects(_id=group_id).first()
        return group

    @classmethod
    def create_new_announcement(cls, resp):
        """Create a new announcement object"""
        new_announcement = Announcement()
        new_announcement["description"] = resp["description"]
        return new_announcement
