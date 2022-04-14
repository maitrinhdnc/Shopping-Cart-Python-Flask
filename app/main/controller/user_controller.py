from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import UserService

api = UserDto.api
_user = UserDto.user

@api.route('/')
class UserList(Resource):
    @api.expect(_user, validate=True)
    @api.response(201, 'User Successfully Created')
    def post(self):
        """Create A New User """
        data = request.json
        return UserService.save_new_user(data)



