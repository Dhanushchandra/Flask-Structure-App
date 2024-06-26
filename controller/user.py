import pymongo.errors
from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from model.userSchema import UserSchema
from exceptions.userExceptions import UserAlreadyExistError


class UserController:
    def __init__(self, mongo):
        self.mongo = mongo
        self.userschema = UserSchema()

    def saveuser(self):
        data = request.json
        user = self.mongo.db.users.insert_one(data)
        return "save"

    def getusers(self):
        result = []
        data = self.mongo.db.users.find()
        for doc in data:
            result.append(
                {'_id': str(doc['_id']), 'username': str(doc['username'])})
        return result

    def getuser(self, id):
        data = self.mongo.db.users.find_one_or_404({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "User not found"}), 404

    def updateuser(self, id):
        data = request.json
        if data:
            updated = self.mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
            if updated:
                return "updated"

    def deleteuser(self, id):
        deleted = self.mongo.db.users.delete_one({'_id': ObjectId(id)})
        if deleted:
            return "deleted"

    def userregister(self):
        try:
            data = self.userschema.load(request.get_json())
            username = data.get("username")
            email = data.get("email")
            password = generate_password_hash(data.get("password"))
            isExist = self.mongo.db.users.find_one({'email': email})
            if isExist:
                raise UserAlreadyExistError(email)
            self.mongo.db.users.insert_one({'username': username,'email': email, 'password': password})
            return jsonify({
                "msg": "user saved successfully"
            }), 201
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except UserAlreadyExistError as e:
            return e.error()
        except pymongo.errors.PyMongoError as e:
            return jsonify({'error': str(e)}), 500

    def userlogin(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = self.mongo.db.users.find_one_or_404({'email': email})
        if user and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token)
        else:
            return jsonify({
                'messege': "Invalid username or password"}), 401

    def proctedroute(self):
        current_user = get_jwt_identity()
        userexist = self.mongo.db.users.find_one({
            "email": current_user
        })
        if userexist:
            return jsonify(logged_in=current_user)
        else:
            return jsonify({
                "msg": "Not Authorized"
            })
