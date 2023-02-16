from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import random
import json
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def cafe_to_dict(cafe):
    cafe = {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "seats": cafe.seats,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
    }
    return cafe


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=['GET'])
def random_cafe():
    random_id = random.randint(0, db.session.query(Cafe).count())
    cafe = db.session.query(Cafe)[random_id]
    return jsonify(cafe_to_dict(cafe))


@app.route("/all", methods=['GET'])
def all():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe_to_dict(cafe) for cafe in cafes])


@app.route("/search", methods=['GET'])
def search():
    location = request.args.get('location')
    cafes = db.session.query(Cafe).filter(Cafe.location == location)
    if cafes.count() > 0:
        return jsonify(cafes=[cafe_to_dict(cafe) for cafe in cafes])
    else:
        return jsonify(error={f"Not Found": f"Sorry we dont have a location in {location}"})


@app.route("/add", methods=['POST'])
def add():
    new_cafe = Cafe()
    request_attributes = request.args.to_dict()

    for key, value in request_attributes.items():
        if value == "true" or value == "false":
            exec(f"new_cafe.{key} = {bool(value)}")
        else:
            exec(f"new_cafe.{key} = '{value}'")
    try:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(success={"response": "Successfully added new cafe."})

    except exc.SQLAlchemyError:
        return jsonify(error={"response": "An error has occurred, please check your query"})


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
