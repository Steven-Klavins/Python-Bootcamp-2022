from flask import Flask, render_template
import requests

app = Flask(__name__)


def get_blog_data():
    try:
        response = requests.get("https://api.npoint.io/eb88574a126d526b4a03")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return []


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

@app.route('/post/<int:post_id>')
def post(post_id):
    blog = [blog for blog in get_blog_data() if int(blog["id"]) == post_id][0]
    return render_template("post.html", header_image="post-sample-image.jpg", blog=blog, page_title=blog["title"])