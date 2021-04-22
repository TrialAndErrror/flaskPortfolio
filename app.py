import os
from datetime import datetime

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

db_path = f'sqlite:///{os.path.join(os.getcwd(), "resume.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '$3cret_D3bug'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('resume/home.html')


@app.route('/about')
def about():
    return render_template('resume/home/about.html')


@app.route('/projects')
def projects():
    return render_template('resume/portfolio/portfolio.html')


@app.route('/resume')
def edit_resume():
    jobs = Job.query.all()
    schools = School.query.all()

    return render_template('resume/resume/wade.html', job_entries=jobs, school_entries=schools)


if __name__ == '__main__':
    app.run(debug=True)
