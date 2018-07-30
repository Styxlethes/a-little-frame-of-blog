from . import auth
from app.main.__init__ import main

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_login import logout_user, login_user

from app.models import User, db
from ..email import send_email


@auth.route('/register', methods=['POST', 'GET'])
def register():
    # 判断用户是否已经注册
    from .forms import RegistrationForm
    form = RegistrationForm()
    if form.validate():
        try:
            # user = User(nickname='nike', email='nike@qq.com')
            user = User(
                nickname=form.nickname.data, email=form.email.data,
                password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, '确认账户', 'auth/email/comfirm',
                       user=user, token=token)
            flash('注册邮件已发送至您的邮箱，请查收')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            flash('创建用户失败')
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页

    # 导入表单处理方法
    from .forms import LoginForm
    form = LoginForm()
    # 验证表单数据格式是否正确
    if form.validate():
        # 根据表格数据对数据库进行查询，有则返回User对象，否则返回None
        user = User.query.filter_by(nickname=form.nickname.data).first()
        # 查询该用户的密码是否正确
        if user is None or user.check_password(form.password.data):
            # 如果密码不正确或者用户名不存在
            flash('用户名不存在或者密码')
            return redirect(url_for('auth.login'))
        # 当用户名与密码都正确时，保持登录状态
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录下的是跳转至登录页面的地址
        next_page = request.args.get('next')
        # 如果next_page不存在则返回首页
        # if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
        # 登陆后要么重定向到主页，要么重定向到跳转前的页面
        return redirect(next_page)
        # 闪现出现的信息
        flash('用户登录的用户名为：%s ' % form.username.data)
        flash('是否记住我:%s' % form.remember_me.data)
        # 重定向到主页
        return(redirect(url_for('main.index')))
    return render_template('auth/login.html', form=form)


# 登出路由
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.comfirmed:
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for(main.index))
    return render_template('auth/unconfirmed.html')
