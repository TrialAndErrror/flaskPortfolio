import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager

from portfolio.resume.forms import JobForm, SchoolForm

app = Flask(__name__, template_folder='templates')

db_path = f'sqlite:///{os.path.join(os.getcwd(), "portfolio.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '$3cret_D3bug'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from portfolio.resume.routes import resume      # noqa E402
from portfolio.auth.routes import auth          # noqa E402
from portfolio.main.routes import main          # noqa E402
from portfolio.projects.routes import proj  # noqa E402

app.register_blueprint(resume)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(proj)
