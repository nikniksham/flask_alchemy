import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    User = orm.relation("Jobs", back_populates='user')
    department = orm.relation("Departments", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} Пользователь {self.id} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
