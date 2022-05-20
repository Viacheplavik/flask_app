from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from main import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class MainMenu(db.Model):
    __tablename__ = 'main_menu'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(50))
    url = sa.Column(sa.String(50))

    def __repr__(self):
        return f"<menu point {self.id}>"


class Posts(db.Model):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(50), unique=True)
    text = sa.Column(sa.String(500), nullable=False)
    url = sa.Column(sa.String(30), unique=True)
    time = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<post {self.id}>"


class Users(db.Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20))
    email = sa.Column(sa.String(30), unique=True)
    psw = sa.Column(sa.String(50), nullable=False)
    avatar = sa.Column(sa.BLOB, nullable=True)
    time = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<user {self.id}>"
