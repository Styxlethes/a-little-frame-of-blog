from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    nickname = StringField('昵称', validators=[
                           DataRequired(message='type your name')])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[
                             DataRequired(message='type your password')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('repeat password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('registration')

    # 校验用户名是否重复
    def validate_username(self, nickname):
        user = User.query.filter_by(nickname=nickname.data).first()
        if user:
            raise ValidationError('用户名重复，请重新输入')

    # 校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱重复，请重新输入')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('旧密码', validators=[DataRequired()])
    newpassword = PasswordField(
        '新密码', validators=[DataRequired(), EqualTo('repeatpassword')])
    repeatpassword = PasswordField('重复新密码', validators=[DataRequired()])
    submit = SubmitField('跟新密码')


class ForgetPasswordRequestForm(FlaskForm):
    email = StringField('输入您账号的邮箱', validators=[
                        DataRequired(), Email(), Length(1, 16)])
    submit = SubmitField('确认发送')


class ForgetPasswordForm(FlaskForm):
    newpassword = PasswordField('输入您的新密码', validators=[DataRequired()])
    repeatpassword = PasswordField(
        '重复您的新密码', validators=[DataRequired(), EqualTo('newpassword')])
    submit = SubmitField('确认新密码')


class ChangeEmailRequestForm(FlaskForm):
    newemail = StringField('新的邮箱地址', validators=[
                           DataRequired(), Email(), Length(1, 16)])
    password = PasswordField('您当前账号的密码', validators=[DataRequired()])
    submit = SubmitField('确认更新邮箱')

    def validate_newemail(self, newemail):
        user = User.query.filter_by(newemail=newemail).first()
        if not user:
            raise ValidationError('该邮箱已注册')
