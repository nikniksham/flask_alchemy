from flask import Flask, render_template, request, make_response
from flask_login import LoginManager, login_user, login_manager, login_required, logout_user, current_user
from werkzeug.utils import redirect
import random
from data import db_session
from data.LoginForm import LoginForm
from data.WorksForm import WorksForm
from data.forms import RegisterForm
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/colonist.sqlite")
    c = False
    if c:
        with open('last_number.txt', 'r') as f:
            last_number = int(f.read())
        with open('last_number.txt', 'w') as f:
            f.write(str(last_number + 3))
        for i in range(last_number, last_number + 3):
            user = User()
            user.name = f'Колонист № {i}'
            user.age = random.choice(range(16, 66))
            user.speciality = 'cleaner'
            user.address = f'module {random.choice(range(1, 101))}'
            user.email = f'happy_colonist{i}@spaceX.com'
            session = db_session.create_session()
            session.add(user)
            session.commit()
            print('new_colonist')
            job = Jobs()
            job.team_leader = 'Scott Ridley'
            job.job = f'deployment of residential module {random.choice(range(1, 101))}'
            job.collaborators = f"{i - 1}, {i}, {i + 1}"
            job.is_finished = False
            job.work_size = f'{random.choice(range(5, 11))} hours'
            session = db_session.create_session()
            session.add(job)
            session.commit()
            print('new_job')
    app.run(port=8000)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


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
        user.about = form.about.data
        user.set_password(form.password.data)
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


@app.route('/login/', methods=['GET', 'POST'])
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
        jobs.is_finished = form.is_finished.data
        current_user.User.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('works.html', title='Добавление новости',
                           form=form)


def new_chef():
    session = db_session.create_session()
    user = User()
    user.surname = 'Scott'
    user.name = 'Ridley'
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    session.add(user)
    session.commit()


def new_job():
    session = db_session.create_session()
    jobs = Jobs(team_leader=5, job='deployment of residential modules 1 and 2', work_size=15,
                collaborators='2, 3', is_finished=False)
    session.add(jobs)
    session.commit()


if __name__ == '__main__':
    main()