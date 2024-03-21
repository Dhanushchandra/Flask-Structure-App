from bson import ObjectId
from flask import request, jsonify


class UserController:
    def __init__(self, mongo):
        self.mongo = mongo

    def saveuser(self):
        data = request.json
        self.mongo.db.users.insert_one(data)
        return "save"

    def getusers(self):
        result = []
        data = self.mongo.db.users.find()
        for doc in data:
            result.append(
                {'_id': str(doc['_id']), 'name': str(doc['name']), 'age': str(doc['age']),
                 'college': str(doc['college'])})
        return result

    def getuser(self,id):
        data = self.mongo.db.users.find_one_or_404({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "User not found"}), 404

    def updateuser(self,id):
        data = request.json
        if data:
            updated = self.mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
            if updated:
                return "updated"

    def deleteuser(self,id):
        deleted = self.mongo.db.users.delete_one({'_id': ObjectId(id)})
        if deleted:
            return "deleted"

