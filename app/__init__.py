from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
ckeditor = CKEditor()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login.init_app(app)
    ckeditor.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)


    return app