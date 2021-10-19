# pylint: disable=no-member
"""CRUD REST-API For Product"""
from models.Product import Product as product_model
from flask_restful import Resource, reqparse, abort
from mongoengine import ValidationError

product_args = reqparse.RequestParser()
product_args.add_argument("_id", type=str, help="Product ID")
product_args.add_argument("title", type=str, help="Product Name")
product_args.add_argument("description", type=str, help="Product Description")
product_args.add_argument("price", type=float, help="Product Price")
product_args.add_argument("quantity", type=int, help="Product Quantity")
product_args.add_argument("imageURL", type=str, help="Product Image URL")
product_args.add_argument(
    "itemIds", type=str, help="A List of the Item Ids", action="append"
)


class Product(Resource):
    """CRUD for accessing/manipulating a single product document"""

    def get(self, product_id):
        """Handles get request for retrieving a single product"""
        product = product_model.objects(_id=product_id)
        if len(product) == 0:
            abort(404)
        return product.to_json(), 200

    def post(self):
        """Handles the post request and creates a new product"""
        new_product = product_model(**product_args.parse_args())
        try:
            new_product.save()
        except ValidationError:
            abort(400, message="Error creating product document")
        return 201

    # NOTE this assumes that the userProduct does not contain None values
    # As such all fields should be required
    def put(self, product_id):
        """Handles the put request to update a single product"""
        user_product = product_model(**product_args.parse_args())
        result = product_model.objects(_id=product_id).update_one(
            title=user_product.title,
            description=user_product.description,
            price=user_product.price,
            quantity=user_product.quantity,
            imageURL=user_product.imageURL,
            itemIds=user_product.itemIds,
        )
        # If no product has been added or updated

        if result == 0:
            abort(404, message="Error updating product")
        return 200

    def delete(self, product_id):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        # If product can't be found then abort
        if len(product) == 0:
            abort(404, message="Can not delete product")
        else:
            product.delete()
        return 202


class Products(Resource):
    """CRUD for accessing/manipulating a multiple product document"""

    def get(self):
        """Handles the get request and returns all the products in the collection"""
        products = product_model.objects.all()
        return products.to_json(), 200
