from flask import (
    render_template,
    request,
    redirect,
    flash,
    abort,
    url_for,
    make_response
)
from flask_login import (
    current_user,
    login_required,
    logout_user,
    login_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from UserLogin import UserLogin
from forms import RegisterForm, LoginForm
from main import app, dbase


@app.route("/")
def index():
    print(__name__)
    return render_template('index.html', menu=dbase.get_menu(), posts=dbase.get_posts_announce())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Error adding an article', category='error')
            else:
                flash('The article was added successfully', category='success')
        else:
            flash('Error adding an article', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title="Adding an article")


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            user_login = UserLogin().create(user)
            rm = form.remember.data
            login_user(user_login, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Invalid login/password pair", "error")
    return render_template("login.html", menu=dbase.get_menu(), title="Authorization", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        psw_hash = generate_password_hash(request.form['psw'])
        res = dbase.add_user(form.name.data, form.email.data, psw_hash)
        if res:
            flash("You have successfully registered", "success")
            return redirect(url_for('login'))
        else:
            flash("Error adding to the database", "error")

    return render_template("register.html", menu=dbase.get_menu(), title="Registration", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out of your account", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_menu(), title="Profile")


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("Avatar Update error", "error")
                flash("Avatar updated", "success")
            except FileNotFoundError as e:
                flash(f"File reading error: {e}", "error")
        else:
            flash("Avatar Update error", "error")

    return redirect(url_for('profile'))
