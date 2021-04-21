import os


from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

db_path = f'sqlite:///{os.path.join(os.getcwd(), "login.db")}'
print(f'Database path: {db_path}')
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SECRET_KEY'] = '$3cret_D3bug'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(60))


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


@app.route('/resume/edit')
def edit_resume():
    pass

if __name__ == '__main__':
    app.run(debug=True)
