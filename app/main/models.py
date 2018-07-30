# from datetime import datetime


# from app.__init__ import db


# class Post(db.Model):
#     __tablename__ = 'post'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(64))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post %s>' % self.body
