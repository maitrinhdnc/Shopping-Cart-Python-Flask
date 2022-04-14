import datetime
from ..config import key
import jwt
from app.main import db
from app.main.model.user import User
from typing import Dict

class UserService:

    def save_new_user(data: Dict[str, str]):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            new_user = User(
                email=data['email'],
                username=data['username'],
                password=data['password'],
                registered_on=datetime.datetime.utcnow()
            )
            UserService.save_changes(new_user)
            return UserService.generate_token(new_user)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409

    def generate_token(user: User):
        try:
            # generate the auth token
            auth_token = UserService.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'Authorization': auth_token.decode()
            }
            return response_object, 201
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return response_object, 401

    @staticmethod
    def encode_auth_token(user_id: str):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def save_changes(data):
        db.session.add(data)
        db.session.commit()

