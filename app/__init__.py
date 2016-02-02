from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from flask.ext.mail import Mail

from multiprocessing import Pool

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

socketio = SocketIO(app)

execution_pool = Pool()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views, models
