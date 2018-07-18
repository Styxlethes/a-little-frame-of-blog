from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           DataRequired(message='type your name')])
    password = PasswordField('password', validators=[
                             DataRequired(message='type your password')])
    remember_me = BooleanField('remember me')
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('repeat password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('registration')
    
	# 校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复，请重新输入')

    # 校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise VlidationError('邮箱重复，请重新输入')
