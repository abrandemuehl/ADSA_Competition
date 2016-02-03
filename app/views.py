from . import app, socketio, execution_pool, login_manager, socketio
from app import app
from flask.ext.socketio import emit
from . import db, models, forms
from flask import render_template, url_for, flash, g, request, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import generate_password_hash
from flask_security.forms import RegisterForm

from util.security import confirm_token, generate_confirmation_token
from util.email import send_email
import csv
import random
import string
import uuid

from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required

security = Security(app, models.user_datastore, register_form=RegisterForm)


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('index'))


@app.route('/')
def index():
    values = {
            "participants": models.Participant.query
                    .filter(models.Participant.last_submission_date)
                    .order_by(models.Participant.best_score).all(),
            }
    return render_template('index.html', **values)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        user = current_user
        submission = models.Submission(submitter_id = user.id)
        file = request.files['file']
        if file and allowed_file(file.filename):
            uid = uuid.uuid1()
            path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.email, str(uid))
            file.save(path)
            submission.file_path = path
            db.session.add(submission)
            db.session.commit()
            return redirect(flask.url_for('testing'), submission=id)
        return render_template('submit.html')
    else:
        return render_template('submit.html')

def registered(email):
    return True

def calculate_score(submission):
    processed = 0
    correct = 0
    score = 0.0
    with open(MASTER_FILE) as master_file:
        master = csv.reader(master_file)
        with open(submission.file_path, 'rb') as csv_file:
            test_reader = csv.reader(csv_file)

            # skip header rows
            master.next() 
            for test_row in islice(test_reader, 1, None):
                master_row = master.next()
                if master_row[-1] == test_row[-1]:
                    correct += 1
                processed += 1
                emit('line_processed', {"correct": correct, "processed": processed})
    score = correct 
    submission.score = score
    db.session.add(submission)
    db.session.commit()
    return submission


def processing_done(submission):
    emit('processing_complete', {'score': submission.score})


def process_submission(submission):
    execution_pool.apply_async(calculate_score, (submission), callback=processing_done)

@app.route('/test/<submission_id>')
@login_required
def test(submission_id):
    submission_id = request.args.get('submission')
    submission = models.Submission.get(submission_id)
    process_submission(submission)
    return render_template('test.html')


























