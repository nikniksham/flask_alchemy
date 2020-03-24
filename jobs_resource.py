from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.jobs import Jobs
from data.users import User
from parser_jobs_api import parser
from put_parser_jobs_api import put_parser
from user_resources import abort_if_user_not_found


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'speciality',
                  'hazard_category', 'is_finished'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    jobs.id = args['id']
                if key == 'team_leader':
                    jobs.team_leader = args['team_leader']
                if key == 'job':
                    jobs.job = args['job']
                if key == 'work_size':
                    jobs.work_size = args['work_size']
                if key == 'collaborators':
                    jobs.collaborators = args['collaborators']
                if key == 'speciality':
                    jobs.speciality = args['speciality']
                if key == 'hazard_category':
                    jobs.hazard_category = args['hazard_category']
                if key == 'is_finished':
                    jobs.is_finished = args['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'speciality',
                  'hazard_category', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(Jobs).get(args['id']):
            abort(400, message='Id already exists')
        abort_if_user_not_found(args['team_leader'])
        jobs = Jobs()
        jobs.user = session.query(User).get(args['team_leader'])
        jobs.id = args['id']
        jobs.team_leader = args['team_leader']
        jobs.job = args['job']
        jobs.work_size = args['work_size']
        jobs.collaborators = args['collaborators']
        jobs.speciality = args['speciality']
        jobs.hazard_category = args['hazard_category']
        jobs.is_finished = args['is_finished']
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
