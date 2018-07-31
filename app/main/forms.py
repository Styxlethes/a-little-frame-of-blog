from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    title = StringField('题目', validators=[DataRequired()])
    body = PageDownField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')
