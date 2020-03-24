from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.users import User
from parser_user_api import parser
from put_parser_user_api import put_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        print(args)
        print(args.keys())
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    user.id = args['id']
                if key == 'surname':
                    user.surname = args['surname']
                if key == 'name':
                    user.name = args['name']
                if key == 'age':
                    user.age = args['age']
                if key == 'position':
                    user.position = args['position']
                if key == 'speciality':
                    user.speciality = args['speciality']
                if key == 'address':
                    user.address = args['address']
                if key == 'email':
                    user.email = args['email']
                if key == 'city_from':
                    user.city_from = args['city_from']
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))
            for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).get(args['id']):
            abort(400, message='Id already exists')
        user = User()
        user.id = args['id']
        user.name = args['name']
        user.surname = args['surname']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.city_from = args['city_from']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
