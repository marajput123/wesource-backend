# pylint: disable=no-member

"""CRUD REST-API For Review"""
from http import HTTPStatus
from flask import json, Blueprint
from flask_restful import Resource, reqparse, abort, Api
from mongoengine import ValidationError
from models.Review import Review as review_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exception_handler


review_blueprint = Blueprint("review_api", __name__)
api = Api(review_blueprint)


review_args = reqparse.RequestParser()
review_args.add_argument("_id", type=str, help="Problem with Review ID value")
review_args.add_argument(
    "reviewer_id", type=str, help="Problem with Reviewer User ID value"
)
review_args.add_argument(
    "reviewee_id", type=str, help="Problem with Reviewee User ID value"
)
review_args.add_argument(
    "description", type=str, help="Problem with Review Content value"
)
review_args.add_argument("rating", type=int, help="Problem with Rating value")


class Review(Resource):
    """CRUD for accessing/manipulating a single review document"""

    @staticmethod
    def get(review_id):
        """Handles get request for retrieving a single review"""
        review = review_model.objects(_id=review_id).first()
        if len(review) == 0:
            abort(HTTPStatus.NOT_FOUND, message="Review could not be found")
        return json.loads(review.to_json()), HTTPStatus.OK

    @staticmethod
    @exception_handler
    @authenticated
    def post(current_user=None):
        """Handles the post request and creates a new review"""
        review = review_args.parse_args()
        new_review = review_model(**review)

        if str(new_review.reviewer_id) != current_user.get_id():
            return {
                "message": "User is not allowed to post review"
            }, HTTPStatus.UNAUTHORIZED

        try:
            new_review.save()
        except ValidationError as err:
            raise MongoErrorHandler(
                ValidationError.to_dict(),  # pylint: disable = no-value-for-parameter
                HTTPStatus.BAD_REQUEST,
            ) from err
        return json.loads(new_review.to_json()), HTTPStatus.OK

    @staticmethod
    @exception_handler
    @authenticated
    def put(review_id, current_user=None):
        """Handles the put request to update a single review"""
        body = {}
        for key, value in review_args.parse_args().items():
            if value is not None:
                body[key] = value

        review = review_model.objects(_id=review_id).first()
        if review and str(review.reviewer_id) != current_user.get_id():
            return {
                "message": "User is not allowed to update review"
            }, HTTPStatus.UNAUTHORIZED

        try:
            review.modify(**body)
        except AttributeError as attr_err:
            raise MongoErrorHandler(
                "Could not update the review", HTTPStatus.NOT_FOUND
            ) from attr_err
        return {"message": f"Review with id of {review_id} updated"}, HTTPStatus.OK

    @staticmethod
    @exception_handler
    @authenticated
    def delete(review_id, current_user=None):
        """Handles the delete request to delete a single product"""
        review = review_model.objects(_id=review_id).first()
        # If product can't be found then abort
        if not review:
            return {"message": "Can not delete review"}, HTTPStatus.BAD_REQUEST

        if str(review.reviewer_id) != current_user.get_id():
            return {
                "message": "User is not allowed to delete review"
            }, HTTPStatus.UNAUTHORIZED

        review.delete()
        return {"message": f"Product with id of {review_id} deleted"}, HTTPStatus.OK


api.add_resource(Review, "/api/review/<string:review_id>", endpoint="review_by_id")
api.add_resource(Review, "/api/review", endpoint="review")
