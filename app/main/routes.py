from app.main import bp
from app import db
from app.models import User, Post
from flask_login import login_required, current_user
from flask import redirect, render_template, url_for, request, flash, session, g
from app.main.forms import CreateForm

import os

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
#    if request.method == 'POST':
#        title = request.form['title']
#        body = request.form['body']
#        error = None
#
#        if not title:
#            error = "Title is required."
#
#        if error is not None:
#            flash(error)
#        else:
#            post = Post(title=title, body=body, author_id=g.user.id)
#            db.session.add(post)
#            db.session.commit()
#
#            return redirect(url_for('main.index'))
#
    form = CreateForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html', title="New Post.", form=form)


@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    template_id = post.template_id
    if post.template_id is None:
        pardir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        basedir = os.path.join(pardir, 'templates/posts')
        template_id = str(id)+'.html'
        template_name = os.path.join(basedir, template_id)
        with open(template_name, 'w') as temp:
            temp.write(post.body)
        post.template_id = template_id
        db.session.commit()

    return render_template('blog_post.html', post=post, title=post.title, temp_id = 'posts/'+template_id)


@bp.route('/user/<int:id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter_by(author_id=id)
    return render_template('user.html', user=user, title=user.username, posts=posts)