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
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'speciality',
                                    'hazard_category', 'is_finished', 'user_id', 'user'))
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
def delete_news(jobs_id):
    session = db_session.create_session()
    print(jobs_id)
    jobs = session.query(Jobs).get(jobs_id)
    print(jobs)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})
