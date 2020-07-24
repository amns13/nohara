from app.auth import bp
from app import db
from models import User
from flask import redirect, render_template, url_for, request


@bp.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    email = request.form['email']

    user = User(username=username, email=email)
    user.set_password(request.form['password'])

    db.session.add(user)
    db.session.commit()