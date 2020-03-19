from os import abort
from flask import Flask, render_template, request, make_response, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect
from data import db_session
from data.departments import Departments
from data.forms import LoginForm, DepartmentsForm
from data.forms import WorksForm
from data.forms import RegisterForm
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/new_colonist.sqlite")
    print('http://127.0.0.1:8080/training/строитель')
    app.run(port=8080)


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
    print(1)
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


if __name__ == '__main__':
    main()