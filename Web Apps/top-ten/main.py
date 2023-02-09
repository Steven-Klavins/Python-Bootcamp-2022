from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
import requests
import os
import sqlite3

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

def add_new_movie(form_data):
    new_movie = Movie(
        title=form_data.title,
        year=form_data.year,
        description=form_data.description,
        rating=form_data.rating,
        ranking=form_data.ranking,
        review=form_data.review,
        img_url=form_data.img_url,
    )

    db.session.add(new_movie)
    db.session.commit()


class EditMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out Of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
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


if __name__ == '__main__':
    app.run(debug=True)
