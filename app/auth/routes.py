from app.auth import bp
from app import db
from app.models import User
from flask import redirect, render_template, url_for, request, flash

from sqlalchemy import or_


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif User.query.filter(or_(User.username == username, User.email == email)).first() is not None:
            error = "Username or Email already exists."

        if error is None:
            user = User(username=username, email=email)
            user.set_password(request.form['password'])

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', title='Register')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    pass
