import sys
from mongoengine import connect
from json import load
from models.Item import Item
from models.Product import Product

from models.User import User

## Replace it with you DB if you need to
MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long


connect(host=MONGODB_URL)

commands = {}

for arg in sys.argv:
    if arg == "cu":
        commands["create_users"] = True
    elif arg == "cp":
        commands["create_products"] = True
    elif arg == "ci":
        commands["create_items"] = True
    elif arg == "du":
        commands["delete_users"] = True
    elif arg == "dp":
        commands["delete_products"] = True
    elif arg == "di":
        commands["delete_items"] = True
    elif arg == "delete_all":
        commands["delete_all"] = True

users = None
with open("./data/users.json") as reader:
    users = load(reader)
items = None
with open("./data/items.json") as reader:
    items = load(reader)
products = None
with open("./data/products.json") as reader:
    products = load(reader)


for key in commands:
    if key == "create_users":
        for user in users:
            User(**user).save()
    if key == "create_products":
        for product in products:
            Product(**product).save()
    if key == "create_items":
        for item in items:
            Item(**item).save()
    if key == "delete_users":
        User.drop_collection()
    if key == "delete_products":
        Product.drop_collection()
    if key == "delete_items":
        Item.drop_collection()
    if key == "delete_all":
        User.drop_collection()
        Item.drop_collection()
        Product.drop_collection()
    