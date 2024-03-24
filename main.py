from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

from controller.user import UserController
from authentication.jwthelper import jwt_middleware

import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

user = UserController(mongo)


@app.route("/register", methods=["POST"])
def register():
    return user.userregister()


@app.route("/login", methods=["POST"])
def login():
    return user.userlogin()


@app.route("/")
@jwt_required()
@jwt_middleware
def getall():
    return user.getusers()


@app.route("/<id>")
@jwt_required()
@jwt_middleware
def get(id):
    return user.getuser(id)


@app.route("/", methods=["POST"])
def post():
    return user.saveuser()


@app.route("/<id>", methods=["PUT"])
@jwt_required()
@jwt_middleware
def update(id):
    return user.updateuser(id)


@app.route("/<id>", methods=["DELETE"])
@jwt_required()
@jwt_middleware
def delete(id):
    return user.deleteuser(id)

@app.route("/content")
@jwt_required()
def protected():
    return user.proctedroute()

app.run(port=3000, debug=True)
