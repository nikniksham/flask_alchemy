import flask
from flask import jsonify, request
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'id', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>',  methods=['GET'])
def get_one_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'speciality',
                                       'hazard_category', 'is_finished', 'user_id',))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'id', 'is_finished', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    if session.query(Jobs).get(request.json.get('id')):
        print('Id already exists')
    session = db_session.create_session()
    jobs = Jobs()
    jobs.job = request.json.get('job')
    jobs.is_finished = request.json.get('is_finished')
    jobs.collaborators = request.json.get('collaborators')
    jobs.work_size = request.json.get('work_size')
    jobs.team_leader = request.json.get('team_leader')
    jobs.user_id = request.json.get('id')
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def put_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    if len(request.json) == 0:
        return jsonify({'error': 'No keys for editing'})
    for key in request.json:
        if key not in ['team_leader', 'job', 'work_size', 'collaborators', 'id', 'is_finished', 'start_date',
                       'speciality', 'hazard_category']:
            return jsonify({'error': 'Invalid key for editing'})
    for key in request.json:
        if key == 'id':
            jobs.id = request.json.get(key)
        if key == 'team_leader':
            jobs.team_leader = request.json.get(key)
        if key == 'job':
            jobs.job = request.json.get(key)
        if key == 'collaborators':
            jobs.collaborators = request.json.get(key)
        if key == 'hazard_category':
            jobs.hazard_category = request.json.get(key)
        if key == 'work_size':
            jobs.work_size = request.json.get(key)
        if key == 'start_date':
            jobs.start_date = request.json.get(key)
        if key == 'speciality':
            jobs.speciality = request.json.get(key)
        if key == 'is_finished':
            jobs.is_finished = request.json.get(key)
    session.commit()
    return jsonify({'success': 'OK'})
