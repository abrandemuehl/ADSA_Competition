from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import EqualTo, Required, Email, InputRequired

class LoginForm(Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember Me', default=False)


class RegisterForm(Form):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])



