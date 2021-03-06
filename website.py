import json
import os
from os import abort
import flask
import requests
from flask import Flask, render_template, request, make_response, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from requests import get
from werkzeug.utils import redirect
import jobs_api
import jobs_resource
import user_resources
import users_api
from data import db_session
import random
from data.departments import Departments
from data.forms import LoginForm, DepartmentsForm, WorksForm, RegisterForm, LoginForm2
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(user_resources.UserListResource, '/api/v2/user')
api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')


def get_list_numbers(number):
    numbers = []
    for i in range(1, number + 1):
        numbers.append(i)
    return numbers


def get_spn(toponym):
    poss = toponym['boundedBy']['Envelope']
    delta_x = str(list(map(float, poss['upperCorner'].split()))[0] - list(map(float, poss['lowerCorner'].split()))[0])
    delta_y = str(list(map(float, poss['upperCorner'].split()))[1] - list(map(float, poss['lowerCorner'].split()))[1])
    return delta_x, delta_y


def main():
    db_session.global_init("db/new_colonist_2.sqlite")
    print('http://127.0.0.1:8100/carousel_2')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8100)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", jobs=jobs, style=url_for('static', filename='css/style.css'))


@app.route("/departments")
def list_departments():
    session = db_session.create_session()
    departments = session.query(Departments).all()
    return render_template("departments.html", departments=departments,
                           style=url_for('static', filename='css/style.css'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.address = form.address.data
        user.speciality = form.speciality.data
        user.position = form.position.data
        user.surname = form.surname.data
        user.set_password(form.password.data)
        user.city_from = form.city_from.data
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test/")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = WorksForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.collaborators = form.collaborators.data
        jobs.work_size = form.work_size.data
        jobs.hazard_category = form.hazard_category.data
        jobs.is_finished = form.is_finished.data
        current_user.User.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('works.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id).first()
    if current_user.id in [jobs.user.id, 1]:
        form = WorksForm()
        if request.method == "GET":
            session = db_session.create_session()
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
            if jobs:
                form.job.data = jobs.job
                form.team_leader.data = jobs.team_leader
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
                form.hazard_category.data = jobs.hazard_category
                form.is_finished.data = jobs.is_finished
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
            if jobs:
                jobs.job = form.job.data
                jobs.team_leader = form.team_leader.data
                jobs.work_size = form.work_size.data
                jobs.collaborators = form.collaborators.data
                jobs.hazard_category = form.hazard_category.data
                jobs.is_finished = form.is_finished.data
                session.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('works.html', title='Редактирование работы', form=form)
    else:
        abort(404)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id).first()
    if current_user.id in [jobs.user.id, 1]:
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            session.delete(jobs)
            session.commit()
        else:
            abort(404)
        return redirect('/')
    else:
        abort(404)


@app.route('/adddepartments',  methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        departments = Departments()
        departments.title = form.title.data
        departments.chief = form.chief.data
        departments.members = form.members.data
        departments.email = form.email.data
        current_user.department.append(departments)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('new_department.html', title='Добавление департамента', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def departments(id):
    session = db_session.create_session()
    departments = session.query(Departments).filter(Departments.id == id).first()
    if current_user.id in [departments.user.id, 1]:
        form = DepartmentsForm()
        if request.method == "GET":
            session = db_session.create_session()
            departments = session.query(Departments).filter(Departments.id == id).first()
            if departments:
                form.title.data = departments.title
                form.chief.data = departments.chief
                form.members.data = departments.members
                form.email.data = departments.email
                session.commit()
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            departments = session.query(Departments).filter(Departments.id == id).first()
            if departments:
                departments.title = form.title.data
                departments.chief = form.chief.data
                departments.members = form.members.data
                departments.email = form.email.data
                session.commit()
                return redirect('/departments')
            else:
                abort(404)
        return render_template('new_department.html', title='Редактирование департамента', form=form)
    else:
        abort(404)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    session = db_session.create_session()
    departments = session.query(Departments).filter(Departments.id == id).first()
    if current_user.id in [departments.user.id, 1]:
        session = db_session.create_session()
        departments = session.query(Departments).filter(Departments.id == id).first()
        if departments:
            session.delete(departments)
            session.commit()
        else:
            abort(404)
        return redirect('/departments')
    else:
        abort(404)


@app.route('/carousel')
def carousel():
    return render_template("carousel.html")


@app.route('/training/<prof>')
def training(prof):
    req = 0
    if 'инженер' in prof.lower().split() or 'строитель' in prof.lower().split():
        req = 1
    return render_template('help_map.html', req=req, img_1=url_for('static', filename='img/col_1.png'),
                           img_2=url_for('static', filename='img/col_2.png'))


@app.route('/list_prof/<list>')
def list_prof(list):
    if list in ['ol', 'ul']:
        return render_template('list_prof.html', list=list, title='list_prof')
    else:
        print('Неверный формат')


@app.route('/answer')
def answer():
    dict_answer = {'surname': '',
                   'name': '',
                   'education': random.choice(['Начальное', 'Среднее-неполное', 'Среднее', 'Среднее-профессинальное',
                                               'Высшее', 'Магистратура']),
                   'profession': random.choice(['Программист', 'Инженер', 'Экзобиолог', 'Пилот', 'Штурман',
                                                'Пилот дронов', 'Врач']),
                   'sex': random.choice(['male', 'female']),
                   'motivation': random.choice(['Хочет приобщиться к чему-то великому', 'Мечтает улететь с земли',
                                                'Обожает красный цвет', 'Хочет развеят скуку', 'Тяга ко знаниям']),
                   'ready': random.choice([True, False])}
    if dict_answer['sex'] == 'male':
        dict_answer['name'] = random.choice(['Николай', 'Василий', 'Анатолий', 'Константин'])
        dict_answer['surname'] = random.choice(['Шамков', 'Торопов', 'Громов', 'Севастьянов', 'Выров'])
    elif dict_answer['sex'] == 'female':
        dict_answer['name'] = random.choice(['Ирина', 'Анна', 'Анастасия', 'Александра', 'Ольга'])
        dict_answer['surname'] = random.choice(['Бабурина', 'Леоновна', 'Кузнецова', 'Циргвава'])
    return render_template('auto_answer.html', dict=dict_answer, title='answer',
                           style=url_for('static', filename='css/style.css'))


@app.route('/login_2', methods=['GET', 'POST'])
def login_2():
    form = LoginForm2()
    if form.validate_on_submit():
        if form.id_captain.data != '' and form.id_astronaut.data != '' and form.password_captain.data != '' and \
           form.password_astronaut.data != '':
            return redirect("/")
        return render_template('login_2.html', message="Ошибка в данных", form=form)
    return render_template('login_2.html', title='Аварийный доступ', form=form,
                           img=url_for('static', filename='img/MARS-2-7.png'))


@app.route('/distribution')
def distribution():
    users = ['Шамков Николай', 'Rjkz Торопов', 'Анатолий Федченко']
    return render_template('distribution.html', users=users)


@app.route('/table/<sex>/<age>')
def table(sex, age):
    category = 'adult'
    if int(age) < 21:
        category = 'young'
    return render_template('table.html', img_1=url_for('static', filename=f'img/{category}.png'),
                           img_2=url_for('static', filename=f'img/{sex}_{category}.png'),
                           style=url_for('static', filename='css/style.css'))


@app.route('/member')
def member():
    with open('templates/user.json', 'r', encoding='utf-8') as fh:
        user = json.load(fh)['Users'][random.choice(range(3))]
    return render_template('member.html', img=url_for('static', filename=f'img/{user["img"]}'), user=user)


@app.route('/users_show/<int:user_id>')
def nostalgia(user_id):
    ans = get(f'http://localhost:8100/api/user/{user_id}').json()
    if ans != {'error': 'Not found'}:
        hometown = ans['user']['city_from']
        user = {"name": ans["user"]["name"], "surname": ans["user"]["surname"], "hometown": hometown}
        a = hometown
        if 'город' not in a.lower().split():
            a = f'город {a}'
        toponym_to_find = ' '.join(a)
        print(a)
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(get_spn(toponym)),
            "l": "sat",
            "pt": ''
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        map_file = "static/img/map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return render_template('nostalgy.html', img=url_for('static', filename='img/map.png'), user=user)
    return render_template('error_404.html', style=url_for('static', filename='css/style.css'))


@app.route('/carousel_2', methods=['POST', 'GET'])
def carousel_2():
    if request.method == 'GET':
        number = 0
        while True:
            if not os.path.exists(f'static/img/mars_{number + 1}.jpg'):
                break
            else:
                number += 1
        return render_template('carousel_2.html', numbers=get_list_numbers(number), help=0)
    if request.method == 'POST':
        f = request.files['file']
        number = 1
        while True:
            if not os.path.exists(f'static/img/mars_{number}.jpg'):
                with open(f'static/img/mars_{number}.jpg', 'wb') as file:
                    file.write(f.read())
                break
            else:
                number += 1
        return render_template('carousel_2.html', numbers=get_list_numbers(number),
                               filename=url_for('static', filename=f'img/mars_{number}.jpg'), help=1)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
