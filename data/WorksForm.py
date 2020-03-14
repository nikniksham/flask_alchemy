from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class WorksForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = TextAreaField("Главный")
    work_size = StringField("Объём работы")
    collaborators = TextAreaField('Участники')
    is_finished = BooleanField("Завершена ли работа?")
    submit = SubmitField("Применить")
