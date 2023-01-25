from flask import Flask, render_template
import requests

app = Flask(__name__)


# Return all blog data as a JSON from npoint.
def get_blogs():
    try:
        response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
        blogs_json = response.json()
        return blogs_json
    except requests.exceptions.RequestException as e:
        return {}


@app.route('/')
def home():
    blogs = get_blogs()
    return render_template("index.html", blogs=blogs)


@app.route('/<int:post_id>')
def post(post_id):
    blogs = get_blogs()
    blog = [blog for blog in blogs if blog["id"] == post_id]
    return render_template("post.html", blog=blog[0])


if __name__ == "__main__":
    app.run(debug=True)
