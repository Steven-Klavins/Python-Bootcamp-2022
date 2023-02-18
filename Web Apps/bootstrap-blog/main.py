from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
import requests
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)

EMAIL = "sample-email@email.com"
SMTP_PROVIDER = "smtp.gmail.com"
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = StringField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Attempt to retrieve blog data.
def get_blog_data():
    return []


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


@app.route('/')
def home():
    blogs = db.session.query(BlogPost).all()
    return render_template("index.html", header_image="home-bg.jpg", blogs=blogs, page_title="Welcome to my blog!")

@app.route('/new-post')
def new_post():
    return render_template("make-post.html", header_image="home-bg.jpg", page_title="Create a new blog post")


@app.route('/about')
def about():
    return render_template("about.html", header_image="about-bg.jpg", page_title="About")


@app.route('/contact')
def contact():
    return render_template("contact.html", header_image="contact-bg.jpg", page_title="Contact")


@app.route('/thanks')
def thanks():
    return render_template("message.html", header_image="contact-bg.jpg",
                           page_title="Message sent!")


@app.route('/sorry')
def sorry():
    return render_template("message.html", header_image="contact-bg.jpg",
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
    print()
    return render_template("post.html", header_image="post-sample-image.jpg", blog=blog, page_title=blog.title)
