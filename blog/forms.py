from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('PasswordField', validators=[DataRequired()])
    submit=SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    content = TextAreaField('Content')
    submit = SubmitField('Save')
    picture  = FileField('Blog Picture', validators=[FileAllowed(['jpg', 'png'])])

class PostPortfolioForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    youtube_link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField('Save')
