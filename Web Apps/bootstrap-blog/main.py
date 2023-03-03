from flask import Flask, g, render_template, request, redirect, url_for, abort
import os
import smtplib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_login import LoginManager
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor, CKEditorField
from forms import CreatePostForm, CreateUserForm, LoginForm
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

EMAIL = "sample-email@email.com"
SMTP_PROVIDER = "smtp.gmail.com"
ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db = sqlite3.connect("blog.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, email varchar(250) NOT NULL UNIQUE, password varchar(250) "
#                "NOT NULL, name varchar(250) NOT NULL)")

# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.id is not 1:
            abort(403, description="This action is for admins only.")
        return f(*args, **kwargs)

    return decorated_function


# Add new blog to DB
def process_blog_form_to_model(form_data):
    blog = BlogPost(
        title=form_data.title.data,
        subtitle=form_data.subtitle.data,
        date=datetime.today().strftime("%d %B, %Y"),
        body=form_data.body.data,
        author=form_data.author.data,
        img_url=form_data.img_url.data,
    )
    return blog


# Process updated blog data
def update_blog(blog, updated_blog):
    blog.title = updated_blog.title
    blog.subtitle = updated_blog.subtitle
    blog.date = updated_blog.date
    blog.body = updated_blog.body
    blog.author = updated_blog.author
    blog.img_url = updated_blog.img_url


# Send the contact form email.
def send_contact_email(email_data):
    message = f"From: {email_data['name']} \n " \
              f"Email: {email_data['email']} \n " \
              f"Tel: {email_data['phone']} \n " \
              f"\n {email_data['message']}"
    email_body = f"Subject:Message from {email_data['name']} \n\n {message}"
    try:
        with smtplib.SMTP(SMTP_PROVIDER) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=os.environ.get("SMTP_PASSWORD"))
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=email_body)
            return True
    except smtplib.SMTPResponseException as e:
        print(e)
        return False


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Home page
@app.route('/')
def home():
    blogs = db.session.query(BlogPost).all()
    return render_template("index.html", header_image="/static/images/home-bg.jpg", blogs=blogs,
                           page_title="Welcome to my blog!")


# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8)
        )

        if User.query.filter_by(email=form.email.data).first():
            return render_template("login.html",
                                   header_image="/static/images/home-bg.jpg", form=form,
                                   error="That email is already registered with us, please login",
                                   page_title="Register")
        else:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
    else:
        return render_template("register.html", header_image="/static/images/home-bg.jpg", form=form,
                               page_title="Register")

    return render_template("register.html", header_image="/static/images/home-bg.jpg", form=form, page_title="Register")


# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return render_template("login.html", form=form, error="Invalid Password")
        else:
            return render_template("login.html", form=form, error="Email Not Found")
    else:
        return render_template("login.html", form=form, header_image="/static/images/home-bg.jpg",
                               page_title="Welcome Back!")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# New blog page
@app.route('/new-post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_blog = process_blog_form_to_model(form)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("make-post.html", header_image="/static/images/home-bg.jpg",
                               page_title="Create a new blog post",
                               form=form)


# Blog edit page
@app.route('/edit-post/<int:post_id>', methods=['POST', 'GET'])
@login_required
@admin
def edit_post(post_id):
    blog = db.session.query(BlogPost).get(post_id)
    form = CreatePostForm(
        title=blog.title,
        subtitle=blog.subtitle,
        date=blog.date,
        body=blog.body,
        author=blog.author,
        img_url=blog.img_url,
    )
    if form.validate_on_submit():
        updated_blog = process_blog_form_to_model(form)
        update_blog(blog, updated_blog)
        db.session.commit()
        return redirect(url_for('post', post_id=blog.id))
    else:
        return render_template("make-post.html", header_image=blog.img_url, blog=blog,
                               page_title=f"Edit {blog.title}", form=form)


# Delete blog post route
@app.route('/delete-post/<int:post_id>')
@login_required
@admin
def delete_post(post_id):
    blog = db.session.query(BlogPost).get(post_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('home'))


# About page
@app.route('/about')
def about():
    return render_template("about.html", header_image="/static/images/about-bg.jpg", page_title="About")


# Contact page
@app.route('/contact')
def contact():
    return render_template("contact.html", header_image="/static/images/contact-bg.jpg", page_title="Contact")


# Contact form confirmation
@app.route('/thanks')
def thanks():
    return render_template("message.html", header_image="/static/images/contact-bg.jpg",
                           page_title="Message sent!")


# Error page for failed contact form submissions
@app.route('/sorry')
def sorry():
    return render_template("message.html", header_image="/static/images/contact-bg.jpg",
                           page_title="Sorry something went wrong!")


# Gather the contact form data and send the email, if successful redirect the user to
# the thank-you page, else send them to sorry something went wrong page.
@app.route('/contact-form', methods=['POST'])
def contact_form():
    email_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "message": request.form['message']
    }

    email_sent = send_contact_email(email_data)
    if email_sent:
        return redirect(url_for('thanks'))
    else:
        return redirect(url_for('sorry'))


# Individual post pages.
@app.route('/post/<int:post_id>')
def post(post_id):
    blog = db.session.query(BlogPost).get(post_id)
    return render_template("post.html", header_image=blog.img_url, blog=blog, page_title=blog.title)
