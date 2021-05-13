from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from portfolio.config import Config
from portfolio.resume.forms import JobForm, SchoolForm

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from portfolio.resume.routes import resume  # noqa E402
    from portfolio.auth.routes import auth      # noqa E402
    from portfolio.main.routes import main      # noqa E402
    from portfolio.projects.routes import proj  # noqa E402

    app.register_blueprint(resume)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(proj)

    return app
