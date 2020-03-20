import flask
from flask import jsonify, request
from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/user')
def get_user():
    session = db_session.create_session()
    user = session.query(User).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                    'city_from'))
                 for item in user]
        }
    )


@blueprint.route('/api/user/<int:user_id>',  methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    print(user_id)
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                       'city_from'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'city_from', 'password']):
        return jsonify({'error': 'Missing some keys to create, you need keys to create:'
                                 'id, surname, name, age, position, speciality, address, email, city_from, password'})
    if session.query(User).get(request.json.get('id')):
        print('Id already exists')
    session = db_session.create_session()
    user = User()
    user.job = request.json.get('job')
    user.is_finished = request.json.get('is_finished')
    user.collaborators = request.json.get('collaborators')
    user.work_size = request.json.get('work_size')
    user.team_leader = request.json.get('team_leader')
    user.user_id = request.json.get('id')
    user.set_passwor(request.json.get('password'))
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    if len(request.json) == 0:
        return jsonify({'error': 'No keys for editing'})
    for key in request.json:
        if key not in ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from']:
            return jsonify({'error': 'Invalid key for editing'})
    for key in request.json:
        if key == 'id':
            user.id = request.json.get(key)
        if key == 'surname':
            user.surname = request.json.get(key)
        if key == 'name':
            user.name = request.json.get(key)
        if key == 'age':
            user.age = request.json.get(key)
        if key == 'position':
            user.position = request.json.get(key)
        if key == 'speciality':
            user.speciality = request.json.get(key)
        if key == 'address':
            user.address = request.json.get(key)
        if key == 'speciality':
            user.speciality = request.json.get(key)
        if key == 'email':
            user.email = request.json.get(key)
        if key == 'city_from':
            user.city_from = request.json.get(key)
    session.commit()
    return jsonify({'success': 'OK'})
