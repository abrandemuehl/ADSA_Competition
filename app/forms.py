from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import EqualTo, Required, Email, InputRequired, regexp



class SubmissionForm(Form):
    csv = FileField('Submission', validators=[Required(), regexp('^.+.csv$')])
