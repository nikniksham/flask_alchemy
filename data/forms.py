from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = TextAreaField("Адрес", validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class WorksForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = TextAreaField("Главный", validators=[DataRequired()])
    work_size = StringField("Объём работы", validators=[DataRequired()])
    collaborators = TextAreaField('Участники', validators=[DataRequired()])
    is_finished = BooleanField("Завершена ли работа?")
    submit = SubmitField("Применить")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

