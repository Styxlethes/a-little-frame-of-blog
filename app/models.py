from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin  # 用于管理用户类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from hashlib import md5
from markdown import markdown
import bleach


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
    name = db.Column(db.String(64))

    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BLOG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            # pass

    def __repr__(self):
        return '<用户名:%s>' % self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
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
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True

    def generate_reset_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True

    def generate_change_email_token(self, new_email, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        db.session.commit()
        return True

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/acvatar/{}?d=indention'.format(digest, size)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     nickname=forgery_py.internet.user_name(),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     about_me=forgery_py.lorem_ipsum.sentence())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Integer)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderater': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = role[r][0]
            role.default = role[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    body = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body_html = db.Column(db.Text)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %s>' % self.body

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentence(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     user_id=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_change_body(target, value, oldvalue, inititor):
        allowed_tag = ['a', 'abbr', 'acronym', 'b', 'blockquote'
                       'code', 'em', 'i', 'pre', 'strong', 'ul',
                       'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkifier(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tag, strip=True))


db.event.listen(Post.body, 'set', Post.on_change_body)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disable = db.Column(db.Boolean)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    @staticmethod
    def on_change_body(target, value, oldvalue, inititor):
        allowed_tag = ['a', 'abbr', 'acronym', 'b'
                       'code', 'em', 'i', 'strong']
        target.body_html = bleach.linkifier(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tag, strip=True))
