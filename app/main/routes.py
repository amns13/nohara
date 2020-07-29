from app.main import bp
from app import db
from app.models import User, Post
from app.auth.routes import login_required 
from flask import redirect, render_template, url_for, request, flash, session, g

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()

            return redirect(url_for('main.index'))

    return render_template('create.html', title="New Post.")