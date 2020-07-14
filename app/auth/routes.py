from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
#from flask_babel import _
#from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app import mongo, login
#from app.models import User
#from app.auth.email import send_password_reset_email
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({username: form.username.data})
        if user is None or not check_password_hash(user[password_hash], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        mongo.db.users.insert_one({username:form.username.data, 
                email:form.email.data, password:password_hash})
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',
                           form=form)


@login.user_loader
def load_user(id):
    return mongo.db.users.find_one({_id: id})                          