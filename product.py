from models.Product import Product as productModel
from flask_restful import Resource, reqparse, abort

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
    def get(self, product_id):
        product = productModel.objects(_id=product_id)
        if len(product) == 0:
            abort(404)
        return product.to_json(), 200

    def post(self):
        newProduct = productModel(**product_args.parse_args())
        newProduct.save()
        return 201

    # NOTE this assumes that the userProduct does not contain None values
    # As such all fields should be required
    def put(self, product_id):
        userProduct = productModel(**product_args.parse_args())
        try:
            productModel.objects(_id=product_id).update_one(
                title=userProduct.title,
                description=userProduct.description,
                price=userProduct.price,
                quantity=userProduct.quantity,
                imageURL=userProduct.imageURL,
                itemIds=userProduct.itemIds,
            )
        except Exception as e:
            print(e)
            abort(404)
        return 200

    def delete(self, product_id):
        product = productModel.objects(_id=product_id)
        if len(product) == 0:
            abort(404)
        else:
            product.delete()
        return 202


class Products(Resource):
    def get(self):
        products = productModel.objects.all()
        return products.to_json(), 200
