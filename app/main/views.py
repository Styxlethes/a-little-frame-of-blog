from . import main

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Post
from ..email import send_email
from ..models import db


'''
每次改动数据库都需要执行
1:flask db migrate -m 'something you just doing'    里头写你要干嘛，作为日志存在
2:flask db upgrade
'''


@main.route('/')
@main.route('/index', methods=['POST', 'GET'])
def index():
    from .forms import PostForm
    form = PostForm()
    if form.validate():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    # page = request.args.get('page', 1, type=int)
    # paginate方法为sqlal提供的一个专门用于创建多页的方法
    # pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
    #     page, per_page=25, error_out=False)
    # posts = pagination.items
    # return render_template('index.html', form=form, posts=posts, pagination=pagination)
    return render_template('index.html', form=form, posts=posts)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(nickname=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/confirm')
@login_required
def resend_email(self):
    token = current_user.gennerate_confirmation_token()
    send_email(current_user.email, '确认您的邮箱',
               'auth/email/confirm', user=current_user, token=token)
    flash('确认邮件已发送')
    return redirect(url_for('main.index'))


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])
