from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"{self.title} by {self.author}"


# db = sqlite3.connect("movies-collection.db") cursor = db.cursor() cursor.execute("CREATE TABLE movies (id INTEGER
# PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, year INTEGER NOT NULL, description varchar(250) NOT NULL,
# rating FLOAT NOT NULL, ranking INTEGER NOT NULL, review varchar(500) NOT NULL, img_url varchar(250))")

def add_new_movie(data):
    print(data)
    new_movie = Movie(
        title=data['original_title'],
        year=int(data['release_date'][:4]),
        description=data["overview"],
        rating=0.0,
        ranking=0,
        review="None",
        img_url=f"https://image.tmdb.org/t/p/original{data['poster_path']}",
    )

    db.session.add(new_movie)
    db.session.commit()


def look_up_movie(title):

    params = {
        "api_key": os.getenv('TMDB_API_KEY'),
        "query": title,
        "include_adult": True
    }

    try:
        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=params)
        response.raise_for_status()
        data = response.json()
        hashed_data = [{"id": movie['id'], "title": movie['title'], "date": movie['release_date']} for movie in data['results']]
        return hashed_data
    except requests.exceptions.RequestException as e:
        print(e)
        return []


def look_up_id(movie_id):

    params = {
        "api_key": os.getenv('TMDB_API_KEY'),
    }

    try:
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(e)
        return False


class EditMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out Of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddMovieForm(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route("/edit<int:movie_id>", methods=['POST', 'GET'])
def edit(movie_id):
    movie = Movie.query.get(movie_id)
    form = EditMovieForm()
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        print(form.rating.data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        form.rating.data = movie.rating
        form.review.data = movie.review
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete<int:movie_id>", methods=['GET'])
def delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movies = look_up_movie(form.movie_title.data)
        return render_template("select.html", movies=movies)
    else:
        return render_template("add.html", form=form)


@app.route("/select<int:movie_id>", methods=['POST', 'GET'])
def select(movie_id):
    movie = look_up_id(movie_id)
    add_new_movie(movie)
    movie_added = db.session.query(Movie).filter_by(title=movie['title']).first()
    return redirect(url_for('edit', movie_id=movie_added.id))


if __name__ == '__main__':
    app.run(debug=True)
