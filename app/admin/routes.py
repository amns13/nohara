from app.admin import bp
from app import db
from app.models import User
from flask import redirect, url_for, current_app, flash


@bp.route('/create_default_admin')
def create_default_admin():
    if User.query.filter_by(role=0).count() == 0:
        username = current_app.config['ADMIN_USER']
        email = current_app.config['ADMIN_EMAIL']
        admin = User(username=username, email=email, role=0, status=1)
        admin.set_password(current_app.config['ADMIN_PW'])
        db.session.add(admin)
        db.session.commit()
        flash("Default admin user created.")
    else:
        flash("Admin already exists.")
    return redirect(url_for('main.index'))