from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.title} by {self.author}"


def add_new_book_entry(form_data):
    book = Book(
        title=form_data.book_name.data,
        author=form_data.book_author.data,
        rating=form_data.rating.data
    )
    db.session.add(book)
    db.session.commit()


class BookForm(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    print(Book.query.all())
    return render_template("index.html", books=Book.query.all(), title="My Books")


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        add_new_book_entry(form)
        return redirect(url_for('home'))

    return render_template("add.html", form=form, title="Add")


@app.route("/delete/<int:book_id>", methods=['POST', 'GET'])
def delete(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit/<int:book_id>", methods=['POST', 'GET'])
def edit(book_id):
    book = Book.query.get(book_id)
    form = BookForm()

    if form.validate_on_submit():
        book.title = form.book_name.data
        book.author = form.book_author.data
        book.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))
    else:
        form.book_name.data = book.title
        form.book_author.data = book.author
        form.rating.data = int(book.rating)
        return render_template("edit.html", form=form, title="Edit")


if __name__ == "__main__":
    app.run(debug=True)
