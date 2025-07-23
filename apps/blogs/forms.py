from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class BlogForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    content_md = TextAreaField('本文 (Markdown)', validators=[DataRequired()])
    submit = SubmitField('投稿')