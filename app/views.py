from . import app, socketio, execution_pool, login_manager, socketio
from app import app
from flask.ext.socketio import emit
from . import db, models, forms
from flask import render_template, url_for, flash, g, request, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import generate_password_hash

from util.security import confirm_token, generate_confirmation_token
from util.email import send_email
import csv
import random
import string
import uuid


# for i in range(10):
#     temp = models.Participant(name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)),best_score=random.random(),email=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)))
#     db.session.add(temp)


# db.session.commit()
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('index'))


@app.route('/')
def index():
    values = {
            "participants": models.Participant.query.filter(models.Participant.last_submission_date).order_by(models.Participant.best_score).all(),
            }
    return render_template('index.html', **values)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.Participant.query.filter_by(email=form.email.data).first_or_404()
        if(user.check_password(generate_password_hash(form.password.data, app.config['BCRYPT_HASH_SALT']))):
            if not login_user(user, remember=form.remember_me):
                flash('Email does not exist. Please register', 'error')
                return render_template('login.html', form=form)
            return redirect(next or url_for('index'))
        else:
            flash('Email or password incorrect', 'error')
    return render_template('login.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            id = uuid.uuid1()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.email, ))
            return redirect(flask.url_for('testing'), submission=id)


@app.route('/confirm/<token>')
def confirm(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.')
    user = models.Participant.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('login'))

def registered(email):
    return True

@app.route('/register', methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        if models.Participant.query.filter_by(email=form.email.data).count() != 0:
            flash("User already registered. Please sign in", 'error')
            return redirect(url_for('login'))
        info = registered(form.email)
        if info:
            pass_hash = generate_password_hash(form.password.data, app.config['BCRYPT_HASH_SALT'])
            user = models.Participant(
                    email=form.email.data,
                    pass_hash=pass_hash,
                    confirmed=False,
                    )
            db.session.add(user)
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm', token=token, _external=True)
            html = render_template('confirmation_email.html', confirm_url=confirm_url)
            subject = 'Confirm Your Account'
            send_email(user.email, subject, html)
            flash("Confirmation Email Sent", 'success')
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print("No info")
            flash("You are not registered for the summit!", 'success')
            return redirect(url_for('index'))

    print("invalid form")
    print(form.email.data)
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(flask.url_for('index'))


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


























