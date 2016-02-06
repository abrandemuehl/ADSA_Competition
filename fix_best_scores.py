#!flask/bin/python



from app import db, models




for user in models.Participant.query.all():
    for submission in user.submissions:
        if submission.score > user.best_score:
            user.best_score = submission.score
            db.session.add(user)
    db.session.commit()
