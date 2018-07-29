from . import app
from flask import render_template, flash, redirect, url_for, request
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db


@app.route('/')
@app.route('/index')
# 必须登录后才能访问主页，会自动跳到登录页
@login_required
def index():
    return render_template('index.html', title='welcome')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # 导入表单处理方法
    from .forms import LoginForm
    form = LoginForm()
    # 验证表单数据格式是否正确
    if form.validate_on_submit():
        # 根据表格数据对数据库进行查询，有则返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 查询该用户的密码是否正确
        if user is None or not user.check_password(form.password.data):
            # 如果密码不正确或者用户名不存在
            flash('用户名不存在或者密码')
            return redirect(url_for('login'))
        # 当用户名与密码都正确时，保持登录状态
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录下的是跳转至登录页面的地址
        next_page = request.args.get('next')
        # 如果next_page不存在则返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 登陆后要么重定向到主页，要么重定向到跳转前的页面
        return redirect(next_page)
        # 闪现出现的信息
        flash('用户登录的用户名为：%s ' % form.username.data)
        flash('是否记住我:%s' % form.remember_me.data)
        # 重定向到主页
        return(redirect(url_for('index')))
    return render_template('login.html', title='login', form=form)

# 登出路由


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    # 判断用户是否已经注册
    print('---------1------------')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    from app.forms import RegistrationForm
    form = RegistrationForm()
    print('---------2------------')
    if form.validate_on_submit():
        print('--------3-------------')
        print('---------4------------')
        try:
            user = User(username='nike', email='nike@qq.com')
            # user = User(username=form.username.data, email=form.email.data)
            user.set_password('123456')
            db.session.add(user)
            db.session.commit()
            print('OK')
            flash('注册成功，欢迎成为用户')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash('创建用户失败')
    print('-------5-----------')
    return render_template('register.html', title='register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    print(username)
    user = User.query.filter_by(username=username).first_or_404()
    print(user.username)
    posts = [
        {'author': user, 'body': '测试Post#1号'},
        {'author': user, 'body': '测试Post#2号'}
    ]
    return render_template('user.html', user=user, posts=posts)
