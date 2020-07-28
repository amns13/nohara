import functools
from app.auth import bp
from app import db
from app.models import User
from flask import redirect, render_template, url_for, request, flash, session, g

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
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = None

        if not username or not password:
            error = "Please enter Username and Password."
        else:
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                error = "Incorrect Username or password."

        if error is None:
            # session is a dict that stores data across requests. When validation succeeds, 
            # the user’s id is stored in a new session. The data is stored in a cookie that 
            # is sent to the browser, and the browser then sends it back with subsequent requests.
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('main.index'))

        flash(error)
    
    return render_template('auth/login.html', title='Sign In')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view