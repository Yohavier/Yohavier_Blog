from flask import render_template, url_for, redirect, flash, request, abort
from sqlalchemy import desc
from blog import app, db, bcrypt
from blog.models import Post, Admin, Video
from blog.forms import LoginForm, PostForm
from flask_login import login_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.order_by(desc(Post.date_posted)).all()
    latest_post = Post.query.order_by(desc(Post.date_posted)).first() 
    return render_template('home.html', posts=posts, latest_post=latest_post, title='Home')

@app.route("/resume")    
def resume():
    return render_template('resume.html', title='Resume')

@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    latest_post = Post.query.order_by(desc(Post.date_posted)).first()
    return render_template('blog_post.html', title=post.title, post=post, latest_post=latest_post)

@app.route("/blog")
def blog():
    posts = Post.query.order_by(desc(Post.date_posted)).all()
    return render_template('blog.html', title="Blog", posts=posts, rows=get_rows(len(posts)))

@app.route("/portfolio")
def portfolio():
    videos = Video.query.order_by(desc(Video.date_posted)).all()
    return render_template('portfolio.html', title="Portfolio", videos=videos, rows=get_rows(len(videos)))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('home'))
        else:
            flash('Login Failed!')
    latest_post = Post.query.order_by(desc(Post.date_posted)).first()
    return render_template('admin_login.html', title='Admin Login', form=form, latest_post=latest_post)


@app.route("/blog/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('New Post')
        return redirect(url_for('home'))
    latest_post = Post.query.order_by(desc(Post.date_posted)).first()
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', latest_post=latest_post)

@app.route("/blog/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        form.description.data = post.description
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.description.data = post.description
    latest_post = Post.query.order_by(desc(Post.date_posted)).first()
    return render_template('create_post.html', latest_post=latest_post, title='Update Post', form=form, legend='Update Post')


@app.route("/blog/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))




def get_rows(amt):
    row_amt = int(amt / 3) + (amt % 3 > 0)
    return row_amt
    