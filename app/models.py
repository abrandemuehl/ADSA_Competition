from app import db, login_manager

from sqlalchemy.ext.hybrid import hybrid_property


class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    best_score = db.Column(db.Float, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    submissions = db.relationship("Submission", backref='participant')
    email = db.Column(db.String, index=True, unique=True)
    pass_hash = db.Column(db.Integer)

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

    @property
    def is_anonymous(self):
        return False
    @property
    def is_active(self):
        return True
    def is_authenticated(self):
        return confirmed

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, server_default=db.func.now())
    submitter_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    # submitter = db.relationship('Participant', back_populates='submissions')


@login_manager.user_loader
def load_user(user_id):
    return Participant.get(user_id)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)
