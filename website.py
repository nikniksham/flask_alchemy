from flask import Flask, render_template
from werkzeug.utils import redirect

from data import db_session
from data.forms import RegisterForm
from data.users import User
from data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.sqlite")
    with open('last_number.txt', 'r') as f:
        last_number = int(f.read())
    with open('last_number.txt', 'w') as f:
        f.write(str(last_number + 3))
    c = False
    if c:
        for i in range(last_number, last_number + 3):
            user = User()
            user.name = f"Пользователь {i}"
            user.about = f"биография пользователя {i}"
            user.email = f"email{i}@email.ru"
            session = db_session.create_session()
            session.add(user)
            news = News(title="Личная запись", content="Эта запись личная",
                        is_private=True)
            user.news.append(news)
            session.commit()
    # for user in session.query(User).all():
    #    print(user)
    # new_chef()
    print('http://127.0.0.1:8080/register/')
    app.run(port=8080)


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(News).all()
    return render_template("index.html", news=news)


@app.route('/register/', methods=['GET', 'POST'])
def reqister():
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
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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


if __name__ == '__main__':
    main()