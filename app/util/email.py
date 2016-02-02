from .. import mail, app
from flask.ext.mail import Message



def send_email(to, subject, html):
    msg = Message(
        subject,
        recipients=[to],
        html=html,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
