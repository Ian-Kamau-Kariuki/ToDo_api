from app import api, Resource, UserModel, fields
from models.UserModel import user_schema, users_schema

# namespace
ns_users = api.namespace('users', description='all tasks regarding users')

user_model = api.model('User', {
    'email': fields.String(),
    'full_name': fields.String(),
    'password': fields.String()
})


@ns_users.route('')
class UsersList(Resource):
    def get(self):
        """return a list of users"""
        return users_schema.dump(UserModel.fetch_all()), 200

    @api.expect(user_model)
    def post(self):
        """add a new user"""
        data = api.payload
        user = UserModel(**data)
        user.save_to_db()
        return user_schema.dump(user), 201


@ns_users.route('/<int:_id>')
class User(Resource):
    def get(self, _id):
        """Retrieve a user by id"""
        user = UserModel.fetch_by_id(_id)
        if user:
            return user_schema.dump(user), 200
        else:
            return {"message": "User does not exist"}, 404

    @api.expect(user_model)
    def put(self, _id):
        """edit a user by id"""
        data = api.payload
        user = UserModel.fetch_by_id(_id)
        if user:
            if u'email' in data:
                user.email = data['email']
            if u'full_name' in data:
                user.full_name = data['full_name']
            if u'password' in data:
                user.password = data['password']
            user.save_to_db()
            return user_schema.dump(user), 200
        return 'User does not exist', 404

    def delete(self, _id):
        """delete a user by id"""
        user = UserModel.fetch_by_id(_id)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted successfully'}
        else:
            return {'message': 'That user does not exist'}
