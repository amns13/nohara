import os
from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_pymongo import PyMongo

from config import Config


login = LoginManager()
mongo = PyMongo()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    mongo.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    return app