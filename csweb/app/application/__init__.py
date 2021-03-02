from flask import Flask
from .app import app as main_blueprint
from .api import app as api_blueprint

from application.database import initialize_database

def create_app():
    app = Flask(__name__)
    # init db
    app.config.from_object('application.config.Config')
    initialize_database(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(main_blueprint)
    return app


app = create_app()
