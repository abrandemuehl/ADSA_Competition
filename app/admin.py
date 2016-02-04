from . import app, root, db
from flask_admin.contrib.sqla import ModelView
from flask.ext.login import current_user

import models

class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True
        return False


root.add_view(MyModelView(models.Role, db.session))
root.add_view(MyModelView(models.Participant, db.session))
root.add_view(MyModelView(models.Submission, db.session))

