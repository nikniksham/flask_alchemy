from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=int)
put_parser.add_argument('name', type=str)
put_parser.add_argument('surname', type=str)
put_parser.add_argument('age', type=int)
put_parser.add_argument('position', type=str)
put_parser.add_argument('speciality', type=str)
put_parser.add_argument('address', type=str)
put_parser.add_argument('email', type=str)
put_parser.add_argument('city_from', type=str)
