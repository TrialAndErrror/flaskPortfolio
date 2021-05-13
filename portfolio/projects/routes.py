from flask import Blueprint, render_template

proj = Blueprint('proj', __name__)


@proj.route('/projects')
def projects():
    return render_template('portfolio/portfolio/portfolio.html')
