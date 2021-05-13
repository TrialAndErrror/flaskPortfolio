from flask import Blueprint, render_template
from portfolio.resume.models import Job, School

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('portfolio/home.html')


@main.route('/about')
def about():
    return render_template('portfolio/home/about.html')


@main.route('/wade')
def show_resume():
    jobs = Job.query.all()
    schools = School.query.all()

    return render_template('portfolio/resume/wade.html', job_entries=jobs, school_entries=schools)
