import functools
from app.auth import bp
from app import db
from app.models import User
from flask import redirect, render_template, url_for, request, flash, session, g
from flask_login import login_user, logout_user, current_user
from sqlalchemy import or_
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse

#@bp.route('/register', methods=['GET', 'POST'])
#def register():
#    if request.method == 'POST':
#        username = request.form['username']
#        email = request.form['email']
#        password = request.form['password']
#        error = None
#
#        if not username:
#            error = "Username is required."
#        elif not email:
#            error = "Email is required."
#        elif not password:
#            error = "Password is required."
#        elif User.query.filter(or_(User.username == username, User.email == email)).first() is not None:
#            error = "Username or Email already exists."
#
#        if error is None:
#            user = User(username=username, email=email)
#            user.set_password(request.form['password'])
#
#            db.session.add(user)
#            db.session.commit()
#
#            return redirect(url_for('auth.login'))
#
#        flash(error)
#
#    return render_template('auth/register.html', title='Register')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',
                           form=form)


#@bp.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method =='POST':
#        username = request.form['username']
#        password = request.form['password']
#        error = None
#        user = None
#
#        if not username or not password:
#            error = "Please enter Username and Password."
#        else:
#            user = User.query.filter_by(username=username).first()
#            if user is None or not user.check_password(password):
#                error = "Incorrect Username or password."
#
#        if error is None:
#            # session is a dict that stores data across requests. When validation succeeds, 
#            # the user’s id is stored in a new session. The data is stored in a cookie that 
#            # is sent to the browser, and the browser then sends it back with subsequent requests.
#            session.clear()
#            session['user_id'] = user.id
#
#            return redirect(url_for('main.index'))
#
#        flash(error)
#    
#    return render_template('auth/login.html', title='Sign In')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        #An attacker could insert a URL to a malicious site in the next argument, so the application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application. To determine if the URL is relative or absolute, I parse it with Werkzeug's url_parse() function and then check if the netloc component is set or not.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    #session.clear()
    #return redirect(url_for('auth.login'))
    logout_user()
    return redirect(url_for('main.index'))


#@bp.before_app_request
#def load_logged_in_user():
#    user_id = session.get('user_id')
#
#    if user_id is None:
#        g.user = None
#    else:
#        g.user = User.query.filter_by(id=user_id).first()
#

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        error = None

        if not email:
            error = 'Email is required.'
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                error = "Email not found."

        if error is None:
            # TO-DO: add logic for password reset mail
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/reset_password_request.html', title='Reset Password.')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)

        db.session.commit()
        flash('Your password has been reset')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', title="Reset Password")