import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))

secrets = None
with open('secrets.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)['PRODUCTION']

class DefaultConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = secrets['SECRET_KEY']
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024 # 50 Mb limit
    ALLOWED_EXTENSIONS = ['txt']
    UPLOAD_FOLDER = os.path.join(basedir, "submissions")
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = secrets['MAIL_USERNAME']
    MAIL_PASSWORD = secrets['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = "no-reply@adsauiuc.com"
    # administrator list
    ADMINS = [secrets['MAIL_USERNAME']]
    SECURITY_PASSWORDLESS = True
    SECURITY_TOKEN_AUTHENTICATION_KEY= secrets['SECRET_KEY']
    SECURITY_TOKEN_MAX_AGE = 604800 # 1 week
    SECURITY_EMAIL_SENDER = 'no-reply@localhost'
    # Temp workaround
    USERS_PATH = os.path.join(basedir, 'users.csv')
    MASTER_FILE = os.path.join(basedir, 'master.txt')
    REGISTRATION_FILE = os.path.join(basedir, 'registration.csv')
    SUPERUSERS = secrets["SUPERUSERS"]
    SECURITY_POST_LOGIN_VIEW = 'index'

class DebugConfig(DefaultConfig):
    DEBUG = True

class ProductionConfig(DefaultConfig):
    DEBUG = False
    SERVER_NAME = "summit.adsauiuc.com/datathon/"
current = DebugConfig()
