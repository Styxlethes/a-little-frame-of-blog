from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # 用于管理用户类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from hashlib import md5


from app.__init__ import login_manager

'''
每次改动数据库都需要执行
1:flask db migrate -m 'something you just doing'    里头写你要干嘛，作为日志存在
2:flask db upgrade
'''


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<用户名:%s>' % self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    '''
     back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，
     关联的是Post中的user_id外键关联的User对象。
     lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;
     joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象;dynamic则不一
     样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相
     应方法才可以获取对象，比如.all()
    '''

    def generate_confirmation_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/acvatar/{}?d=indention'.format(digest, size)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    body = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %s>' % self.body


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
