from flask_sqlalchemy import SQLAlchemy
# from application.database import initialize_database


from flask_migrate import Migrate


db = SQLAlchemy()


def initialize_database(app):
    db.init_app(app)
    Migrate(app, db)
