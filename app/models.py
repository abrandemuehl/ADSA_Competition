from app import app, db, login_manager

from sqlalchemy.ext.hybrid import hybrid_property

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



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
    confirmed_at = db.Column(db.Date)
    active = db.Column(db.Boolean)
    email = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.Date)
    current_login_at = db.Column(db.Date)
    last_login_ip = db.Column(db.String(20))
    current_login_ip = db.Column(db.String(20))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('participant', lazy='dynamic'))

    best_score = db.Column(db.Float, index=True)
    submissions = db.relationship("Submission", backref='participant')
    last_submission_date = db.Column(db.Date)

    @hybrid_property
    def entries_count(self):
        return len(self.submissions)

    @hybrid_property
    def last_submission_date(self):
        return Submission.query.order_by(Submission.date).first()

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, server_default=db.func.now())
    submitter_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    file_path = db.Column(db.String(255), unique=True)
    score = db.Column(db.Float, index=True)

user_datastore = SQLAlchemyUserDatastore(db, Participant, Role)
