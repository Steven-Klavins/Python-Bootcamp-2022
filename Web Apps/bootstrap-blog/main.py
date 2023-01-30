from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
import requests

EMAIL = "sample-email@email.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"

app = Flask(__name__)


# Attempt to retrieve blog data.
def get_blog_data():
    try:
        response = requests.get("https://api.npoint.io/eb88574a126d526b4a03")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return []


# Send the contact form email.
def send_contact_email(email_data):
    message = f"From: {email_data['name']} \n\n " \
              f"Email: {email_data['email']} \n\n " \
              f"Tel: {email_data['phone']} \n\n " \
              f"Message: \n\n {email_data['message']} \n\n"
    email_body = f"Subject:Message from {email_data['name']} \n\n {message}"
    try:
        with smtplib.SMTP(SMTP_PROVIDER) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=email_body)
            return True
    except smtplib.SMTPResponseException as e:
        print(e)
        return False


@app.route('/')
def home():
    blogs = get_blog_data()
    return render_template("index.html", header_image="home-bg.jpg", blogs=blogs, page_title="Welcome to my blog!")


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
    blog = [blog for blog in get_blog_data() if int(blog["id"]) == post_id][0]
    return render_template("post.html", header_image="post-sample-image.jpg", blog=blog, page_title=blog["title"])
