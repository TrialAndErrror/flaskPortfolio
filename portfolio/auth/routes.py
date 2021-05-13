from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, current_user

from portfolio.auth.models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        return render_template('portfolio/home/login.html')
    else:
        flash('Already Logged-in')
        return redirect(url_for('resume.manage_resume'))


@auth.route('/login', methods=['POST'])
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
        return redirect(url_for('auth.login'))

    """
    If nothing wrong, login the user
    """
    login_user(user, remember=remember)
    return redirect(url_for('resume.manage_resume'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
