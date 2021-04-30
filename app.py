import os
from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for, request

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin

from forms import JobForm, SchoolForm

app = Flask(__name__)

db_path = f'sqlite:///{os.path.join(os.getcwd(), "resume.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '$3cret_D3bug'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
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


@app.route('/')
def home():
    return render_template('resume/home.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('resume/home/login.html')


@app.route('/login', methods=['POST'])
def login_post():
    """
    Login user based on credentials in posted form.

    :return: redirect: manage_resume
    """
    name = request.form.get('username')
    password = request.form.get('password')
    remember = True

    user = User.query.filter_by(username=name).first()

    """
    Check for missing user or wrong password
    """
    if not user or not check_password_hash(user.password, password):
        flash('Username or password was incorrect.')
        return redirect(url_for('login'))

    """
    If nothing wrong, login the user
    """
    login_user(user, remember=remember)
    return redirect(url_for('manage_resume'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('resume/home/about.html')


@app.route('/projects')
def projects():
    return render_template('resume/portfolio/portfolio.html')


@app.route('/wade')
def show_resume():
    jobs = Job.query.all()
    schools = School.query.all()

    return render_template('resume/resume/wade.html', job_entries=jobs, school_entries=schools)


@login_required
@app.route('/resume', methods=['GET', 'POST'])
def manage_resume():
    jobs_list = Job.query.all()
    school_list = School.query.all()

    return render_template('resume/resume/view_entries.html', job_entries=jobs_list, school_entries=school_list)


@login_required
@app.route('/resume/job/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    chosen_job: Job = Job.query.get_or_404(job_id)
    form = JobForm()
    """
    If submitting a valid form, copy data and enter into database.
    """
    if form.validate_on_submit():
        chosen_job.job_title = form.job_title.data
        chosen_job.employer = form.employer.data
        chosen_job.important = form.important.data
        chosen_job.location = form.location.data

        chosen_job.start_date = form.start_date.data
        chosen_job.present_job = form.present_job.data
        chosen_job.end_date = form.end_date.data
        chosen_job.important = form.important.data
        chosen_job.location = form.location.data

        chosen_job.line_1 = form.line_1.data
        chosen_job.line_2 = form.line_2.data
        chosen_job.line_3 = form.line_3.data
        chosen_job.line_4 = form.line_4.data
        db.session.commit()
        flash(f'Entry for {chosen_job.job_title} at {chosen_job.employer} updated')
        return redirect(url_for('manage_resume'))

    """
    Fill out form based on existing job data.
    """
    form.job_title.data = chosen_job.job_title
    form.employer.data = chosen_job.employer
    form.important.data = chosen_job.important
    form.location.data = chosen_job.location

    form.start_date.data = chosen_job.start_date
    form.present_job.data = chosen_job.present_job
    form.end_date.data = chosen_job.end_date

    form.line_1.data = chosen_job.line_1
    form.line_2.data = chosen_job.line_2
    form.line_3.data = chosen_job.line_3
    form.line_4.data = chosen_job.line_4

    return render_template('resume/resume/create_job.html', form=form)


@login_required
@app.route('/resume/job/delete/<int:job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    selected_job = Job.query.filter_by(id=job_id).first()
    alert = f'Entry for {selected_job.job_title} at {selected_job   .employer} deleted'
    db.session.delete(selected_job)
    db.session.commit()
    flash(alert)
    return redirect(url_for('manage_resume'))


@login_required
@app.route('/resume/school/edit/<int:school_id>', methods=['GET', 'POST'])
def edit_school(school_id):
    chosen_school: School = School.query.get_or_404(school_id)
    form = SchoolForm()

    if form.validate_on_submit():
        chosen_school.degree = form.degree.data
        chosen_school.school_name = form.school_name.data
        chosen_school.graduation_date = form.graduation_date.data

        chosen_school.line_1 = form.line_1.data
        chosen_school.line_2 = form.line_2.data
        chosen_school.line_3 = form.line_3.data
        chosen_school.line_4 = form.line_4.data

        db.session.commit()
        flash(f'Entry for {chosen_school.degree} at {chosen_school.school_name} updated')
        return redirect(url_for('manage_resume'))

    form.degree.data = chosen_school.degree
    form.school_name.data = chosen_school.school_name
    form.graduation_date.data = chosen_school.graduation_date

    form.line_1.data = chosen_school.line_1
    form.line_2.data = chosen_school.line_2
    form.line_3.data = chosen_school.line_3
    form.line_4.data = chosen_school.line_4

    return render_template('resume/resume/create_school.html', form=form)


@login_required
@app.route('/resume/school/delete/<int:school_id>', methods=['GET', 'POST'])
def delete_school(school_id):
    selected_school: School = School.query.filter_by(id=school_id).first()
    alert = f'Entry for {selected_school.degree} at {selected_school.school_name} deleted'
    db.session.delete(selected_school)
    db.session.commit()
    flash(alert)
    return redirect(url_for('manage_resume'))


@login_required
@app.route('/resume/create_job', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        new_job = Job(
            job_title=form.job_title.data,
            employer=form.employer.data,
            location=form.location.data,
            important=form.important.data,
            start_date=form.start_date.data,
            present_job=form.present_job.data,
            end_date=form.end_date.data,
            line_1=form.line_1.data,
            line_2=form.line_2.data,
            line_3=form.line_3.data,
            line_4=form.line_4.data
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job Created!', 'success')
        return redirect(url_for('manage_resume'))
    return render_template('resume/resume/create_job.html', form=form)


@login_required
@app.route('/resume/create_school', methods=['GET', 'POST'])
def create_school():
    form = SchoolForm()
    if form.validate_on_submit():
        new_job = School(
            school_name=form.school_name.data,
            degree=form.degree.data,
            graduation_date=form.graduation_date.data,
            line_1=form.line_1.data,
            line_2=form.line_2.data,
            line_3=form.line_3.data,
            line_4=form.line_4.data
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job Created!', 'success')
        return redirect(url_for('manage_resume'))
    return render_template('resume/resume/create_school.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
