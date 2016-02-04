#!flask/bin/python
from migrate.versioning import api
from config import current
from app import db
import os.path
SQLALCHEMY_DATABASE_URI = current.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = current.SQLALCHEMY_MIGRATE_REPO
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
