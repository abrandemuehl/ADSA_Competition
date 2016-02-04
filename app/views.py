from . import app, login_manager
from . import db, models
from flask import render_template, url_for, flash, g, request, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_security.forms import RegisterForm


import uuid
import os

from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required

security = Security(app, models.user_datastore, register_form=RegisterForm)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index'))



@app.route('/')
def index():
    values = {
            "participants": models.Participant.query
                    .filter(models.Participant.last_submission_date != None)
                    .order_by(models.Participant.best_score.desc()).all(),
            "current_user": current_user,
            }
    return render_template('index.html', **values)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



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
    try:
        return ((float(master) - float(check)) ** 2, 1)
    except:
        raise ValueError("Could Not Convert Row to Float")

def accumulate(total, current):
    return (total[0] + current[0], total[1] + current[1])


def calculate_score(submission):
    if submission.tested:
        return submission.score
    processed = 0
    score = 0.0
    with open(app.config['MASTER_FILE'], 'r') as master_file:
        with open(submission.file_path, 'r') as test_file:
            output = reduce(accumulate, map(score_row, master_file, test_file))
            print output 
            score = output[0] / output[1]
    submission.score = score
    submission.tested = True
    db.session.add(submission)
    participant = models.Participant.query.get(submission.submitter_id)
    if submission.score < participant.best_score or not participant.best_score:
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
    submission = models.Submission.query.get(submission_id)
    # process_submission(submission)
    score = 0
    error = None
    try:
        score = calculate_score(submission)
    except ValueError as e:
        error = str(e)
    return render_template('test.html', score=score, error=error)







@app.route('/submissions')
@login_required
def submissions():
    submissions = models.Submission.query.filter_by(submitter_id=current_user.id).order_by(models.Submission.date).all()
    return render_template('submissions.html', submissions=submissions)


















