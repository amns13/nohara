from app.admin import bp
from app import db
from app.models import User, Post
from flask import redirect, url_for, current_app, flash
from flask_login import current_user, login_required
import functools


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


def is_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role != 0:
            flash("You don't have priviliges to perform this action.")
            return redirect(url_for('main.index'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def delete_post(post_id):
    post = Post.query.get(post_id)
    post.status = 0
    db.session.commit()
    flash("Post was deleted.")
    return redirect(url_for('main.index'))

