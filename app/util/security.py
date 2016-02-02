from itsdangerous import URLSafeTimedSerializer

from .. import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def generate_confirmation_token(email):
    return ts.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    try:
        email = ts.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email
