from datetime import datetime

from portfolio import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User: {self.username}"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    employer = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    important = db.Column(db.Boolean, nullable=True, default=True)

    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    present_job = db.Column(db.Boolean, nullable=True, default=False)
    end_date = db.Column(db.DateTime, nullable=True)

    line_1 = db.Column(db.String(100), nullable=False)
    line_2 = db.Column(db.String(100), nullable=True)
    line_3 = db.Column(db.String(100), nullable=True)
    line_4 = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Job: {self.job_title} with {self.employer}"


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(50), nullable=False)
    school_name = db.Column(db.String(50), nullable=False)
    graduation_date = db.Column(db.DateTime, nullable=True)

    line_1 = db.Column(db.String(100), nullable=True, default='No Description')
    line_2 = db.Column(db.String(100), nullable=True, default='No Description')
    line_3 = db.Column(db.String(100), nullable=True, default='No Description')
    line_4 = db.Column(db.String(100), nullable=True, default='No Description')

    def __repr__(self):
        return f"School: {self.degree} from {self.school_name}"


class Extra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)

    text = db.Column(db.String(100), nullable=True, default='No Description')

    def __repr__(self):
        return f"Extra ({self.category}): {self.text}"