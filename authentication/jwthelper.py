from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity




def jwt_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization').split(" ")[1]
            if not access_token:
                return jsonify({'message': 'Missing authorization token'}), 401
            get_jwt_identity()
        except Exception as e:
            return jsonify({'message': str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function