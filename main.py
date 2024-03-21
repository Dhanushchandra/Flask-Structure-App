from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from controller.user import UserController

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask1"
mongo = PyMongo(app)

app.config['JWT_SECRET_KEY'] = "autocartrain"
jwt = JWTManager(app)

user = UserController(mongo)


@app.route("/register", methods=["POST"])
def register():
    return user.userregister()


@app.route("/login", methods=["POST"])
def login():
    return user.userlogin()


@app.route("/")
def getall():
    return user.getusers()


@app.route("/<id>")
def get(id):
    return user.getuser(id)


@app.route("/", methods=["POST"])
def post():
    return user.saveuser()


@app.route("/<id>", methods=["PUT"])
def update(id):
    return user.updateuser(id)


@app.route("/<id>", methods=["DELETE"])
def delete(id):
    return user.deleteuser(id)

@app.route("/content")
@jwt_required()
def protected():
    return user.proctedroute()

app.run(port=3000, debug=True)
