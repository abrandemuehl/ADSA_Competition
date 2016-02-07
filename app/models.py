from app import app, db, login_manager, registration

from sqlalchemy.ext.hybrid import hybrid_property

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


import csv

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('participant.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Participant(db.Model, UserMixin):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    confirmed_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    email = db.Column(db.String, index=True, unique=True)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(20))
    current_login_ip = db.Column(db.String(20))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('participant', lazy='dynamic'))
    best_score = db.Column(db.Float, index=True)

    submissions = db.relationship("Submission", backref='participant')
    last_submission_date = db.Column(db.DateTime)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    submitter_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    file_path = db.Column(db.String(255), unique=True)
    score = db.Column(db.Float, index=True)
    tested = db.Column(db.Boolean, default=False)

user_datastore = SQLAlchemyUserDatastore(db, Participant, Role)



@app.before_first_request
def load_registration():
    """
    Make sure that all of the users in the registration are created
    """
    email_col = 26
    # Skip header
    next(registration)
    for row in registration:
        email = row[email_col]
        if Participant.query.filter_by(email=email).count() == 0:
            user_datastore.create_user(email=email)
    db.session.commit()


@app.before_first_request
def add_superuser():
    """
    Add admins
    """
    if Role.query.filter_by(name='superuser').count() == 0:
        role = Role(name='superuser')
        db.session.add(role)
        db.session.commit()
    for superuser in app.config["SUPERUSERS"]:
        if Participant.query.filter_by(email=superuser).count() == 0:
            user_datastore.create_user(email=superuser, roles=[Role(name='superuser')])
            db.session.commit()


