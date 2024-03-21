from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from controller.user import UserController


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask1"
mongo = PyMongo(app)

user = UserController(mongo)

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


app.run(port=3000, debug=True)
