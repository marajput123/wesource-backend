"""User Model"""
from bson.objectid import ObjectId
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import EmailField, IntField, StringField, ListField
from werkzeug.security import generate_password_hash, check_password_hash


from util.decorators.errorHandler import MongoErrorHandler


# pylint: disable=no-member
class User(Document):
    """User Collection"""

    _id = ObjectIdField(default=ObjectId, primary_key=True)
    firstName = StringField(max_length=50, required=True)
    lastName = StringField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True, unique=True)
    username = StringField(max_length=30, min_length=6, required=True, unique=True)
    password = StringField(required=True)  # password hash
    rating = IntField(default=0)
    groupId = ListField(ObjectIdField(db_field="Group"))

    @classmethod
    def get_by_username(cls, username):
        """Retrieve user by username"""
        data = User.objects(username=username).first()
        if data is not None:
            return data
        raise MongoErrorHandler(f"Canot find user with username({username})", 404)

    @classmethod
    def get_by_email(cls, email):
        """Retrieve user by email"""
        data = User.objects(email=email).first()
        if data is not None:
            return data
        raise MongoErrorHandler(
            """Email or password are not correct.
                Please make sure you have entered the correct credentials.""",
            400,
        )

    @classmethod
    def get_by_id(cls, user_id: str):
        """Retrieve user by id"""
        data = User.objects(_id=ObjectId(oid=user_id)).first()
        if data is not None:
            return data
        raise MongoErrorHandler(f"Canot find user with id({user_id})", 404)

    def get_id(self):
        """Return objectId in String format"""
        return str(self._id)

    def hash_password(self, password):
        """Hash given password and stores result in `password` field"""
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Check provided password against hashed password stored in database.

        Returns True if password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
