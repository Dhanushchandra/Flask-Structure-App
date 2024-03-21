from bson import ObjectId
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask1"
mongo = PyMongo(app)


@app.route("/")
def getall():
    result = []
    data = mongo.db.users.find()
    for doc in data:
        result.append(
            {'_id': str(doc['_id']), 'name': str(doc['name']), 'age': str(doc['age']), 'college': str(doc['college'])})
    return result

@app.route("/<id>")
def get(id):
    data = mongo.db.users.find_one_or_404({"_id":ObjectId(id)})
    data["_id"] = str(data["_id"])
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/", methods=["POST"])
def post():
    data = request.json
    mongo.db.users.insert_one(data)
    return "save"


@app.route("/<id>", methods=["PUT"])
def update(id):
    data = request.json
    if data:
        updated = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
        if updated:
            return "updated"


@app.route("/<id>", methods=["DELETE"])
def delete(id):
    deleted = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if deleted:
        return "deleted"


app.run(port=3000, debug=True)
