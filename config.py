import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'caonima'

    # flask-sqlalchemy
    # 此处utf-8是无效的，只有utf8才有效
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:081791@localhost:3376/flask_blog?charset=utf8'
    # SQLALCHEMY_DATABASE_URI='sqlite///'+os.path.join(basedir,'flaskblog.db')
    SQLALCHEMY_TRACK_MODEFICATION = False
    SQLALCHEMY_ECHO = True
