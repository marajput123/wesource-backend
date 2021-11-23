"""Module for populating MongoDB database"""
import sys
from json import load
from mongoengine import connect
from models.Product import Product
from models.User import User
from models.Review import Review
from models.Group import Group

## Replace it with you DB if you need to
MONGODB_URL = "mongodb+srv://capstone:Capstone123@wesourcecluster01.ctf3x.mongodb.net/WesourceDatabase?retryWrites=true&w=majority"  # pylint: disable=line-too-long

connect(host=MONGODB_URL)

commands = {}

for arg in sys.argv:
    if arg == "cu":
        commands["create_users"] = True
    elif arg == "cp":
        commands["create_products"] = True
    elif arg == "cr":
        commands["create_reviews"] = True
    elif arg == "cg":
        commands["create_groups"] = True
    elif arg == "du":
        commands["delete_users"] = True
    elif arg == "dp":
        commands["delete_products"] = True
    elif arg == "dr":
        commands["delete_reviews"] = True
    elif arg == "dg":
        commands["delete_groups"] = True
    elif arg == "delete_all":
        commands["delete_all"] = True

USERS = None
with open(file="./data/users.json", encoding="utf-8") as reader:
    USERS = load(reader)
PRODUCTS = None
with open("./data/products.json", encoding="utf-8") as reader:
    PRODUCTS = load(reader)
REVIEWS = None
with open("./data/reviews.json", encoding="utf-8") as reader:
    REVIEWS = load(reader)
GROUPS = None
with open("./data/groups.json", encoding="utf-8") as reader:
    GROUPS = load(reader)

for key in commands:
    if key == "create_users":
        for user in USERS:
            user = User(**user)
            user.hash_password(user.password)
            user.save()
    if key == "create_products":
        for product in PRODUCTS:
            Product(**product).save()
    if key == "create_reviews":
        for review in REVIEWS:
            Review(**review).save()
    if key == "create_groups":
        for group in GROUPS:
            Group(**group).save()
    if key == "delete_users":
        User.drop_collection()
    if key == "delete_products":
        Product.drop_collection()
    if key == "delete_reviews":
        Review.drop_collection()
    if key == "delete_groups":
        Group.drop_collection()
    if key == "delete_all":
        User.drop_collection()
        Product.drop_collection()
        Review.drop_collection()
        Group.drop_collection()
