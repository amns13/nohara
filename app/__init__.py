import os
from flask import Flask, request, current_app
from flask_login import LoginManager



login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)

    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')