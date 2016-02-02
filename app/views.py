from . import app, socketio, execution_pool, login_manager, socketio
from flask.ext.socketio import emit
from . import db, models, forms
from flask import render_template, url_for, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required

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
            "participants": models.Participant.query.order_by(models.Participant.best_score).all(),
            }
    return render_template('index.html', **values)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if not login_user(user, remember=form.remember_me):
            flash('Email or password incorrect', 'login-error')
            return render_template('login.html', form=form)
        return redirect(next or url_for('index'))
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
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('login'))


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        info = registered(form.email)
        if info:
            user = User(
                    email=form.email,
                    password=form.password.data,
                    confirmed=False,
                    )
            db.session.add(user)
            db.session.commit()
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm', token=token, _external=True)
            html = render_template('confirmation_email.html', confirm_url=confirm_url)
            subject = 'Confirm Your Account'
            send_email(user.email, subject, html)
            flash("Confirmation Email Sent", 'success')
        return redirect(url_for('index'))
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


























