import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))

secrets = None
with open('secrets.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = secrets['SECRET_KEY']



# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = secrets['MAIL_USERNAME']
MAIL_PASSWORD = secrets['MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = secrets['MAIL_USERNAME']

# administrator list
ADMINS = [secrets['MAIL_USERNAME']]

SECURITY_PASSWORD_SALT = secrets['SECURITY_PASSWORD_SALT']

BCRYPT_HASH_SALT = secrets['BCRYPT_HASH_SALT']
