from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login


@login.user_loader
def load_user(id):
    return mongo.db.users.find_one({_id: id})                          