import datetime
import math
import re
from models import Users, Posts, MainMenu
import time
from sqlalchemy import exc
from flask import url_for
from models import db as database
import sqlalchemy as sa
from sqlalchemy.orm import Session

session = Session()


class DBaseQueries:
    def __init__(self, db):
        self.__db = db

    def get_menu(self):
        try:
            res = self.__db.session.query(MainMenu).all()
            if res:
                return res
        except exc.SQLAlchemyError as e:
            print(f"error during menu db request: {e}")
        return []

    def add_post(self, title, text, url):
        pass

    def get_post(self, alias):
        # test
        try:
            res = self.__db.session.query.filter(Posts.url.like(alias)).all()
            if res:
                return res
        except exc.SQLAlchemyError as e:
            print(f"error during post getting: {e}")
        return (
            False, False
        )

    def get_post_announce(self):
        # get tuple without time
        try:
            res = self.__db.session.query(Posts).order_by(Posts.time.desc())
            if res:
                return res
        except exc.SQLAlchemyError as e:
            print(f"error getting posts from db: {e}")
            return False
        return []

    def add_user(self):
        pass

    def get_user(self, user_id):
        try:
            res = self.__db.session.query(Users).filter_by(id=user_id)

            if not res:
                print("user not found")
                return False
            return res
        except exc.SQLAlchemyError as e:
            print(f"Error getting data from the db: {e}")

    def get_user_by_email(self, email):
        # test
        try:
            res = self.__db.session.query(Users).filter_by(email=email).one()
            if not res:
                print("User not found")
                return False
            return res
        except exc.SQLAlchemyError as e:
            print(f"error during getting user by email: {e}")
        return False

    def update_user_avatar(self, avatar, user_id):
        # test
        if not avatar:
            return False
        try:
            binary = sa.BLOB(avatar)
            self.__db.session.query(Users).filter_by(id=user_id).update(avatar=binary)
            session.commit()
        except exc.SQLAlchemyError as e:
            print(f"error in time of avatar updating: {e}")
            return False
        return True


def main():
    dbasequeries = DBaseQueries(database)
    print(dbasequeries.get_menu()[0].title)
    print(dbasequeries.get_user(user_id=1)[0].name)
    # print(datetime.datetime.utcnow())
    print(dbasequeries.get_post_announce()[0].url)


if __name__ == '__main__':
    main()
