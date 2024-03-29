# from datetime import datetime

# from app.__init__ import db

# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from hashlib import md5
# from app.__init__ import login_manager


# class User(UserMixin, db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(128), index=True, unique=True)
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#     about_me = db.Column(db.String(140))
#     last_seen = db.Column(db.DateTime, default=datetime.utcnow)

#     password_hash = db.Column(db.String(256))

#     def __repr__(self):
#         return '<用户名:%s>' % self.nickname

#     @property
#     def password(self):
#         return self._password

#     @password.setter
#     def set_password(self, raw):
#         self.password_hash = generate_password_hash(raw)

#     def check_password(self, raw):
#         if not self.password_hash:
#             return False
#         return check_password_hash(self.password_hash, raw)
#     '''
#      back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，
#      关联的是Post中的user_id外键关联的User对象。
#      lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;
#      joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象;dynamic则不一
#      样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相
#      应方法才可以获取对象，比如.all()
#     '''

#     def avatar(self, size):
#         digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#         return 'http://www.gravatar.com/acvatar/{}?d=indention'.format(digest, size)


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))
