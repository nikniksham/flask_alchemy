from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=int)
put_parser.add_argument('team_leader', type=str)
put_parser.add_argument('job', type=str)
put_parser.add_argument('work_size', type=int)
put_parser.add_argument('collaborators', type=str)
put_parser.add_argument('speciality', type=str)
put_parser.add_argument('hazard_category', type=int)
put_parser.add_argument('is_finished', type=bool)
