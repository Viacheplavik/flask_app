import sqlite3

from flask import Blueprint
from flask import Flask
from flask import (
    request,
    redirect,
    url_for,
    flash,
    render_template,
    session,
    g
)

app = Flask(__name__)

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.list_pubs', 'title': 'Articles List'},
        {'url': '.list_users', 'title': 'Users List'},
        {'url': '.logout', 'title': 'Exit'}]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(_request):
    global db
    db = None
    return _request


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Admin-panel')


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if is_logged():
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid login/password pair')
    return render_template('admin/login.html', title='Admin-panel')


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not is_logged():
        return redirect(url_for('admin.login'))

    logout_admin()

    return redirect(url_for('admin.login'))


@admin.route('/list-pubs')
def list_pubs():
    if not is_logged():
        return redirect(url_for('.login'))

    posts = list()
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            posts = cur.fetchall()
        except sqlite3.Error as e:
            print("Error getting articles from the database " + str(e))

    return render_template('admin/list_pubs.html', title='List of articles', menu=menu, list=posts)


@admin.route('/list-users')
def list_users():
    if not is_logged():
        return redirect(url_for('.login'))

    users = list()
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            users = cur.fetchall()
        except sqlite3.Error as e:
            print("Error getting articles from the database " + str(e))

    return render_template('admin/list_users.html', title='List of articles', menu=menu, list=users)
