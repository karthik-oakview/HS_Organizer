

from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(100))
    message = db.Column(db.String(1000))
    subject = db.Column(db.String(300))
    graduating_year=db.Column(db.Integer)

class Volunteering(db.Model):
    volunteer_seq = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200))
    org_email=db.Column(db.String(150))
    activity =  db.Column(db.String(200))
    approver = db.Column(db.String(200))
    date = db.Column(db.Date)
    description = db.Column(db.String(500))
    hours = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    docref= db.Column(db.String(500))

  

class Honors(db.Model):
    honors_seq = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200))
    award_name = db.Column(db.String(200))
    date = db.Column(db.Date)
    level = db.Column(db.String(30))
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    docref= db.Column(db.String(500))

class Credit(db.Model):
    creditid = db.Column(db.Integer, primary_key=True);
    course_name = db.Column(db.String(200))
    credit_unit= db.Column(db.Numeric)
    weightage = db.Column(db.Integer)
    provider = db.Column(db.String(200))
    classification = db.Column(db.String)
    score = db.Column(db.Numeric)
    grade = db.Column(db.String(1))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    docref= db.Column(db.String(500))

class Job(db.Model):
    job_seq = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200))
    org_email=db.Column(db.String(150))
    role =  db.Column(db.String(200))
    approver = db.Column(db.String(200))
    date = db.Column(db.Date)
    description = db.Column(db.String(500))
    hours = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    docref= db.Column(db.String(500))

class Recommendation(db.Model):
    recommend_seq = db.Column(db.Integer, primary_key=True)
    recommend_name = db.Column(db.String(200))
    recommend_email=db.Column(db.String(150))
    date = db.Column(db.Date)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    docref= db.Column(db.String(500))
    