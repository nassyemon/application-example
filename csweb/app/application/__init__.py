from flask import Flask
from flask_login import LoginManager

from application.database import initialize_database
from application.models import User
from application.models import Owner
from application.models import OwnerData
from .owner import authowner as auth_owner_blueprint
from .auth import auth as auth_blueprint
from .app import app as main_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('application.config.Config')
    initialize_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # loginowner_manager = LoginManager()
    # loginowner_manager.login_view = 'authowner.login'
    # loginowner_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        return User.query.get(str(email))

    # @loginowner_manager.user_loader
    # def load_owner(email):
    #     return Owner.query.get(str(email))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(auth_owner_blueprint)
    app.register_blueprint(main_blueprint)

    return app


app = create_app()
