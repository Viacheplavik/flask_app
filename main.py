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

from FDataBase import FDataBase

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


def get_db():
    '''Соединение с бд, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# MENU = [{'title': 'Установка', 'url': 'install-flask'},
#         {'title': 'Первое приложение', 'url': 'first-app'},
#         {'title': 'Обратная связь', 'url': 'contact'}]


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link.db'):
        g.link_db.close()


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.get_menu(), posts=dbase.getPostAnounce())


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте')


@app.route('/contact', methods=["POST", "GET"])
def contact():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':

        if len(request.form['username']) > 2 and '@' in request.form['email']:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=dbase.get_menu())


@app.errorhandler(404)
def page_not_found(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html', title='Страница не найдена', menu=dbase.get_menu()), 404


@app.route("/login", methods=['POST', 'GET'])
def login():
    db = get_db()
    dbase = FDataBase(db)

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'viacheplavik' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=dbase.get_menu())


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'<h1>Профиль пользователя: {username}</h1>'


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title='Добавление статьи')

@app.route('/post/<int:id_post>')
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', title=title, post=post, menu=dbase.get_menu())
# with app.test_request_context():
#     print(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
