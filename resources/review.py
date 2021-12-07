# pylint: disable=no-member

"""CRUD REST-API For Review"""
from http import HTTPStatus
from bson.objectid import ObjectId
from flask import json, Blueprint, request
from flask_restful import Resource, reqparse, abort, Api
from mongoengine import ValidationError
from models.User import User as user_model
from models.Review import Review as review_model
from util.decorators.auth import authenticated
from util.decorators.errorHandler import MongoErrorHandler, exception_handler
from util.helper.helper_functions import clean_arguments


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

    @exception_handler
    @authenticated
    def post(self, current_user=None):
        """Handles the post request and creates a new review"""
        body = clean_arguments(review_args)
        if "_id" not in body:
            body["_id"] = ObjectId()
        new_review = review_model(**body)

        if str(new_review.reviewer_id) != current_user.get_id():
            return {
                "message": "User is not allowed to post review"
            }, HTTPStatus.UNAUTHORIZED

        try:
            new_review.save()
            reviewee = user_model.objects(_id=new_review.reviewee_id).first()
            reviewee["reviewId"].append(new_review.get_id())
            reviewee["rating"] = self._calculate_rating(reviewee)
            reviewee.save()
        except ValidationError as err:
            raise MongoErrorHandler(
                ValidationError.to_dict(),  # pylint: disable = no-value-for-parameter
                HTTPStatus.BAD_REQUEST,
            ) from err
        return json.loads(new_review.to_json()), HTTPStatus.OK

    @exception_handler
    @authenticated
    def put(self, review_id, current_user=None):
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
            reviewee = user_model.objects(_id=review.reviewee_id).first()
            reviewee["rating"] = self._calculate_rating(reviewee)
            reviewee.save()
        except AttributeError as attr_err:
            raise MongoErrorHandler(
                "Could not update the review", HTTPStatus.NOT_FOUND
            ) from attr_err
        return {"message": f"Review with id of {review_id} updated"}, HTTPStatus.OK

    @exception_handler
    @authenticated
    def delete(self, review_id, current_user=None):
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
        reviewee = user_model.objects(_id=review.reviewee_id).first()
        reviewee["reviewId"].remove(review.get_id())
        reviewee["rating"] = self._calculate_rating(reviewee)
        reviewee.save()
        return {"message": f"Review with id of {review_id} deleted"}, HTTPStatus.OK

    @staticmethod
    def _calculate_rating(user):
        """Caulculate user rating based on all user reviews"""
        rating_sum = 0
        for review_id in user["reviewId"]:
            review = review_model.objects(_id=review_id).first()
            rating_sum += review.rating
        return round(rating_sum / len(user.reviewId), 1)


class Reviews(Resource):
    """CRUD for accessing multiple review document"""

    @staticmethod
    def get(user_id):
        """Handles get request for retrieving all reviews for a user"""

        reviews = review_model.objects(reviewee_id=user_id).all()

        # Return directly if not reviews are found
        if len(reviews) == 0:
            abort(
                HTTPStatus.NOT_FOUND, message="Review for this user could not be found"
            )

        # Replace reviewer_id with user infomation
        json_reviews = []
        for review in reviews:
            reviewer = user_model.objects(_id=review.reviewer_id).first()
            json_review = json.loads(review.to_json())
            json_review["reviewer"] = json.loads(reviewer.to_json())
            del json_review["reviewer_id"]
            json_reviews.append(json_review)

        # Handles pagination
        page_number = request.args.get("page")
        if page_number is not None:
            review_limit = 15
            offset = (int(page_number) - 1) * review_limit

            if len(json_reviews) <= offset:
                paginated_reviews = []
            else:
                paginated_reviews = json_reviews[offset : (offset + review_limit)]

            json_response = {
                "data": paginated_reviews,
                "total_count": len(paginated_reviews),
            }
            return json_response, HTTPStatus.ACCEPTED

        # if no page number is provided get all reviews
        json_response = {
            "data": json_reviews,
            "total_count": len(json_reviews),
        }
        return json_response, HTTPStatus.OK


api.add_resource(Review, "/api/review/<string:review_id>", endpoint="review_by_id")
api.add_resource(Review, "/api/review", endpoint="review")
api.add_resource(
    Reviews, "/api/user/<string:user_id>/reviews", endpoint="reviews_by_user_id"
)
