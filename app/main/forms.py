from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('题目', validators=[DataRequired()])
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')
