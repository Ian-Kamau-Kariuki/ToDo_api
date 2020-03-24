from app import api, Resource, UserModel
from models.UserModel import user_schema, users_schema

# namespace
ns_users = api.namespace('users', description='all tasks regarding users')


@ns_users.route('')
class UsersList(Resource):
    def get(self):
        """return a list of users"""
        return users_schema.dump(UserModel.fetch_all()), 200

    def post(self):
        """add a new user"""
        data = api.payload
        user = UserModel(email=data['email'], full_name=data['full_name'], password=data['password'])
        record = user.create_record();
        return user_schema.dump(record), 201


@ns_users.route('/<int:id>')
class User(Resource):
    def get(self, _id):
        """Retrieve a user by id"""

    def put(self, _id):
        """edit a user by id"""

    def delete(self, _id):
        """delete a user by id"""
