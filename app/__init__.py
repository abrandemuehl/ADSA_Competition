from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_admin import Admin

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

root = Admin(app, name='ADSA Summit', template_mode='bootstrap3')

import csv
registration = csv.reader(open(app.config['REGISTRATION_FILE'], 'r'))

from . import views, models, admin
