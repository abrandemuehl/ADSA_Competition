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
        file = request.files['file']
        if file and allowed_file(file.filename):
            id = uuid.uuid1()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.email, ))
            return redirect(flask.url_for('testing'), submission=id)
        return render_template('submit.html')
    else:
        return render_template('submit.html')

def registered(email):
    return True

def calculate_score(file_path):
    correct = 0
    score = 0.0
    with open(MASTER_FILE) as master_file:
        master = csv.reader(master_file)
        with open(filepath, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if(row[-1] == master[-1]):
                    correct += 1
                emit('line_processed', {'correct': correct})
    return score


def processing_done(result):
    emit('processing_complete', {'score': result})


def process_submission(file_path):
    execution_pool.apply_async(calculate_score, (file_path), callback=processing_done)

@app.route('/test')
@login_required
def test():
    submission_id = request.args.get('submission')
    submission_path = os.path.join(app.config['UPLOAD_FOLDER'])
    process_submission()
    return render_template('test.html')


























