# pylint: disable=no-member

"""CRUD REST-API For Product"""
from flask_restful import Resource, reqparse, abort
from mongoengine import ValidationError
from models.Product import Product as product_model

product_args = reqparse.RequestParser()
product_args.add_argument("_id", type=str, help="Problem with Product ID value")
product_args.add_argument(
    "title", type=str, help="Problem with Product Name validation"
)
product_args.add_argument(
    "description", type=str, help="Problem with Product Description value"
)
product_args.add_argument("price", type=float, help="Problem with Product Price value")
product_args.add_argument(
    "quantity", type=int, help="Problem with Product Quantity value"
)
product_args.add_argument(
    "imageURL", type=str, help="Problem with Product Image URL value"
)
product_args.add_argument(
    "items",
    type=dict,
    help="Problem with the list of the items' value",
    action="append",
)

# https://stackoverflow.com/questions/19234737/nested-validation-with-the-flask-restful-requestparser
# Embedded document validation for item is not working
# embedded_item_args = reqparse.RequestParser()
# embedded_item_args.add_argument(
#     "_id", type=str, help="Problem with Product ID validation", location=("items",)
# )
# embedded_item_args.add_argument(
#     "title", type=str, help="Problem with Product Name validation", location=("items",)
# )
# embedded_item_args.add_argument(
#     "description", type=str, help="Product Description", location=("items",)
# )
# embedded_item_args.add_argument(
#     "price", type=float, help="Product Price", location=("items",)
# )
# embedded_item_args.add_argument(
#     "quantity", type=int, help="Product Quantity", location=("items",)
# )
# embedded_item_args.add_argument(
#     "imageURL", type=str, help="Product Image URL", location=("items",)
# )


class Product(Resource):
    """CRUD for accessing/manipulating a single product document"""

    @staticmethod
    def get(product_id):
        """Handles get request for retrieving a single product"""
        product = product_model.objects(_id=product_id).first()
        if len(product) == 0:
            abort(404)
        return product.to_json(), 200

    @staticmethod
    def post():
        """Handles the post request and creates a new product"""
        product = product_args.parse_args()
        new_product = product_model(**product)
        try:
            new_product.save()
        except ValidationError:
            abort(400, message="Error creating product document")
        return 201

    # NOTE this assumes that the userProduct does not contain None values
    # Since there doesn't seem to be a way to keep original value if new value is None
    # As such (almost) all fields should be required and updated
    @staticmethod
    def put(product_id):
        """Handles the put request to update a single product"""
        user_product = product_model(**product_args.parse_args())
        result = product_model.objects(_id=product_id).update_one(
            title=user_product.title,
            description=user_product.description,
            price=user_product.price,
            quantity=user_product.quantity,
            imageURL=user_product.imageURL,
            items=user_product.items,
        )
        # If no product has been added or updated
        if result == 0:
            abort(404, message="Error updating product")
        return 200

    @staticmethod
    def delete(product_id):
        """Handles the delete request to delete a single product"""
        product = product_model.objects(_id=product_id)
        # If product can't be found then abort
        if len(product) == 0:
            abort(404, message="Can not delete product")
        else:
            product.delete()
        return 200


class Products(Resource):
    """CRUD for accessing/manipulating multiple product document"""

    @staticmethod
    def get():
        """Handles the get request and returns all the products in the collection"""
        products = product_model.objects.all()
        return products.to_json(), 200


# item_args = reqparse.RequestParser()
# item_args.add_argument("_id", type=str, help="Problem with Product ID validation")
# item_args.add_argument("title", type=str, help="Problem with Product Name validation")
# item_args.add_argument("description", type=str, help="Product Description")
# item_args.add_argument("price", type=float, help="Product Price")
# item_args.add_argument("quantity", type=int, help="Product Quantity")
# item_args.add_argument("imageURL", type=str, help="Product Image URL")

# class ProductItem(Resource):
#     """CRUD for accessing/manipulating a product item"""

#     def get(self, item_id):
#         """Handles the get request and returns the specific item in the product item's list"""
#         product_id = request.form["product_id"]
#         item = (
#             product_model.objects.get(_id=product_id).items.filter(_id=item_id).first()
#         )
#         # print(product)
#         # item = product.items(_id=item_id)
#         print(item.to_json())
#         return item.to_json(), 200

#     # Post request can use Product's post method

#     def put(self, product_id, item_id):
#         """Handles the put request and updates a specific product item"""
#         user_item = item_args.parse_args()

#         embedded_item_list = (
#             product_model.objects(_id=product_id).first().items.filter(_id=item_id)
#         )
#         embedded_item_list.update(
#             title=user_item.title,
#             description=user_item.description,
#             price=user_item.price,
#             quantity=user_item.quantity,
#             imageURL=user_item.imageURL,
#         )
#         embedded_item_list.save()
#         return 200

#     def delete(self, item_id):
#         return


# class ProductItems(Resource):
#     """CRUD for accessing/manipulating product items in the list"""

#     def get(self):
#         return
