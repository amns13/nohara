from app.main import bp
from app import db
from app.models import User, Post, Comment, PostLike
from flask_login import login_required, current_user
from flask import redirect, render_template, url_for, request, flash, session, g, current_app, send_from_directory, jsonify
from app.main.forms import CreateForm, CommentForm
from flask_ckeditor import upload_fail, upload_success
from time import time

import re
import os

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)


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
    if request.method == 'POST' and form.cancel.data:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html', title="New", form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.author_id != current_user.id:
        flash("You don't have access to the requested page.")
        return redirect(url_for('main.index'))
        
    form = CreateForm()
    if request.method == 'POST' and form.cancel.data:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data 
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    return render_template('create.html', title="Edit", form=form)


@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    comments = Comment.query.filter_by(post_id=id).all()
    likes = PostLike.query.filter_by(post_id=id).count()
    form = CommentForm()
    return render_template('blog_post.html', post=post, comments=comments, title=post.title, likes=likes, form=form)


@login_required
@bp.route('/post/<int:postid>/add_comment/', methods=['POST'])
def add_comment(postid):
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        comment = Comment(body=body, post_id=postid, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': '{}'.format(form.body.data)})
    return jsonify({'message': 'An error occurred.'})


@login_required
@bp.route('/like/<int:post_id>/<action>', methods=['POST'])
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    #return redirect(request.referrer)
    likes = PostLike.query.filter_by(post_id=post_id).count()
    return jsonify({'count': likes})


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id=user.id).order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, title=user.username, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@bp.route('/ckeditor_upload', methods=['POST'])
def ckeditor_upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    timestamp = re.sub('\.', '', str(time()))
    filename = str(current_user.id) + timestamp + f.filename
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], filename))
    url = url_for('main.uploaded_files', filename=filename)
    return upload_success(url=url)