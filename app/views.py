from . import app, login_manager
from . import db, models
from flask import render_template, url_for, flash, g, request, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_security.forms import RegisterForm
from sqlalchemy import asc

import numpy as np

import uuid
import os

from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required

security = Security(app, models.user_datastore, register_form=RegisterForm)
from datetime import datetime
import pytz

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('file_too_large.html')


tz = pytz.timezone('US/Central')
@app.route('/')
def index():
    values = {
            "participants": models.Participant.query
                    .filter(models.Participant.submissions.any())
                    .order_by(models.Participant.best_score.desc()).all(),
            "current_user": current_user,
            "utc": pytz.utc,
            "timezone": tz

            }
    return render_template('index.html', **values)

deadline = datetime(2016, 2, 7, 1, 30, 0, 0)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if(datetime.utcnow() > deadline):
        return render_template('deadline.html')
    if request.method == 'POST':
        user = current_user
        submission = models.Submission(submitter_id = user.id)
        file = request.files['file']
        if file:
            uid = uuid.uuid1()

            path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.email, str(uid))
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(path, "w") as outfile:
                file.save(outfile)
            submission.file_path = path
            db.session.add(submission)
            db.session.commit()
            return redirect(url_for('test', submission_id=submission.id))
        return render_template('submit.html')
    else:
        return render_template('submit.html')

def registered(email):
    return True

def score_row(master, check):
    return (master - check) ** 2

def accumulate(total, current):
    return (total[0] + current[0], total[1] + current[1])

def calculate_score(submission):
    if submission.tested:
        return submission.score
    processed = 0
    score = 0.0
    master_file = np.loadtxt(app.config['MASTER_FILE'])
    master = master_file.tolist()
    error = ValueError("Input file must be a text or csv file with %s lines" % len(master))
    try:
        test_file = np.loadtxt(submission.file_path)
    except Exception:
        raise error
    # Fancy one liner to compare all of the rows
    # Abandoned for lack of error checking
    # output = reduce(accumulate, map(score_row, master_file, test_file))
    # score = output[0] / output[1]
    test = test_file.tolist()
    if(len(test) > len(master)):
        raise error
    elif(len(test) < len(master)):
        raise error
    for i in range(len(master)):
        master_row = master[i]
        test_row = test[i]
        score += score_row(master_row, test_row)

    print score
    score = score / len(master)
    print score

    score = np.exp(-1 * score) * 100
    submission.score = score
    submission.tested = True
    db.session.add(submission)
    db.session.commit()
    participant = models.Participant.query.get(submission.submitter_id)
    if participant.best_score:
        if submission.score > participant.best_score:
            participant.best_score = submission.score
    else:
        participant.best_score = submission.score

    participant.last_submission_date = db.func.now()
    db.session.add(participant)
    db.session.commit()
    return submission.score


def processing_done(submission):
    print(submission.score)
    emit('processing_complete', {'score': submission.score})

def process_submission(submission):
    execution_pool.apply_async(calculate_score, (submission), callback=processing_done)

@app.route('/test/<submission_id>')
@login_required
def test(submission_id):
    submission = models.Submission.query.filter_by(submitter_id=current_user.id, id=submission_id).first()
    if not submission:
        return redirect(url_for('index'))
    # process_submission(submission)
    score = 0
    error = None
    try:
        score = calculate_score(submission)
    except Exception as e:
        db.session.delete(submission)
        db.session.commit()
        error = str(e)
        print str(e)
    return render_template('test.html', score=score, error=error)







@app.route('/submissions')
@login_required
def submissions():
    submissions = models.Submission.query.filter_by(submitter_id=current_user.id).order_by(models.Submission.date).all()
    time_data = {
            "utc": pytz.utc,
            "timezone": pytz.timezone("US/Central")
            }
    return render_template('submissions.html', submissions=submissions, **time_data)


















