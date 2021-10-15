"""Module for populating MongoDB database"""
import sys
from json import load
from mongoengine import connect
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

USERS = None
with open(file="./data/users.json", encoding="utf-8") as reader:
    USERS = load(reader)
ITEMS = None
with open("./data/items.json", encoding="utf-8") as reader:
    ITEMS = load(reader)
PRODUCTS = None
with open("./data/products.json", encoding="utf-8") as reader:
    PRODUCTS = load(reader)


for key in commands:
    if key == "create_users":
        for user in USERS:
            User(**user).save()
    if key == "create_products":
        for product in PRODUCTS:
            Product(**product).save()
    if key == "create_items":
        for item in ITEMS:
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
