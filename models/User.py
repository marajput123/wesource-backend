"""User Model"""
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import EmailField, IntField, StringField
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    """User Collection"""

    _id = ObjectIdField(default=ObjectId())
    firstName = StringField(max_length=50, required=True)
    lastName = StringField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True, unique=True)
    username = StringField(max_length=30, min_length=6, required=True, unique=True)
    password = StringField(required=True)  # password hash
    rating = IntField(default=0)


    def hash_password(self, password):
        """Hash given password and stores result in `password` field"""
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Check provided password against hashed password stored in database.

        Returns True if password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
