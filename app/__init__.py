from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    return app