from flask.ext.wtf import Form

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
