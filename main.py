from flask import Flask
from flask import (
    render_template,
    url_for,
    request,
    flash,
    session,
    redirect,
    abort,
    g
)


import sqlite3
import os

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'LSDJFHSDGFHSG'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'LSDJFHSDGFHSG'
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогательная функция для создания таблиц бд'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


menu = [{'name': 'Установка', 'url': 'install-flask'},
        {'name': 'Первое приложение', 'url': 'first-app'},
        {'name': 'Обратная связь', 'url': 'contact'}]


@app.route('/')
def index():
    db = get_db()
    return render_template('index.html', title='Про Flask', menu=menu)


def get_db():
    '''Соединение с бд, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link.db'):
        g.link_db.close()

@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте')


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':

        if len(request.form['username']) > 2 and '@' in request.form['email']:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'viacheplavik' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'<h1>Профиль пользователя: {username}</h1>'


# with app.test_request_context():
#     print(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
