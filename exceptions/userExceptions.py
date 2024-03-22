from flask import jsonify


class UserAlreadyExistError(Exception):
    def __init__(self,email):
        self.email = email

    def error(self):
        return jsonify({'error': f'User with email {self.email} already exists',
                        'email': self.email
                        }), 409