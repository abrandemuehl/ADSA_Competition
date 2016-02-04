from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_admin import Admin

from .middleware import ReverseProxied, StreamConsumingMiddleware

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object('config.current')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

root = Admin(app, name='ADSA Summit', template_mode='bootstrap3')

import csv
registration = csv.reader(open(app.config['REGISTRATION_FILE'], 'r'))

if not app.config['DEBUG']:
    # Use headers for proxying
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    # Use streams for file uploads
    app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

from . import views, models, admin
