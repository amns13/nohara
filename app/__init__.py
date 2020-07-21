from config import Config
from flask import Flask


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)



    return app