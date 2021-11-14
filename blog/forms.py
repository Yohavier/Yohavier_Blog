from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('PasswordField', validators=[DataRequired()])
    submit=SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = CKEditorField('Description')
    content = CKEditorField('Content')
    submit = SubmitField('Save')

