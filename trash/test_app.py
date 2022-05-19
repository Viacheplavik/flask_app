from flask import Flask
from flask import render_template, make_response, redirect, url_for

app = Flask(__name__)

menu = [
    {"title": "Главная", "url": "/"},
    {"title": "Добавить статью", "url": "/add_post"}
]


#
# @app.route('/')
# def index():
#     content = render_template('index.html', menu=menu, posts=[])
#     res = make_response(content)
#     res.headers['Content-Type'] = 'text/html'
#     res.headers['Server'] = 'flasksite'
#     return res

# @app.route("/")
# def index():
#     img = None
#     with app.open_resource(app.root_path + "/static/images/ava.png", mode='rb') as f:
#         img = f.read()
#     if img is None:
#         return "None image"
#     res = make_response(img)
#     res.headers['Content-Type'] = 'image/png'
#     return res

@app.route('/')
def index():
    res = make_response("<h1>Main page</h1>", 200, {'Content-type': 'text/plain'})
    return res


@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


@app.before_first_request
def before_first_request():
    print("before first request() called")


@app.before_request
def before_request():
    print("before request() called")


@app.after_request
def before_request(response):
    print("after request() called")
    return response


@app.teardown_request
def teardown_request(response):
    print("teardown request() called")
    return response


if __name__ == '__main__':
    app.run(debug=True)
