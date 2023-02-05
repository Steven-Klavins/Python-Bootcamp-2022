from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, url
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)


# Add to CSV

def add_entry_to_csv(form_data):
    csv_data_entry = f"{form_data.cafe_name.data}," \
                     f"{form_data.location_google_maps.data}," \
                     f"{form_data.opening_time.data}," \
                     f"{form_data.closing_time.data}," \
                     f"{form_data.coffee_rating.data}," \
                     f"{form_data.wifi_strength_rating.data}," \
                     f"{form_data.power_socket_availability.data}"

    with open('cafe-data.csv', 'a', encoding='utf-8') as fd:
        fd.write("\n" + csv_data_entry)


# Add forum

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location_google_maps = StringField('Cafe location on Google maps (URL)', validators=[DataRequired(), url()])
    opening_time = StringField('Opening Time e.g 8:00AM', validators=[DataRequired()])
    closing_time = StringField('Opening Time e.g 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', validators=[DataRequired()], choices=[
        ('☕', '☕'),
        ('☕☕', '☕☕'),
        ('☕☕☕', '☕☕☕'),
        ('☕☕☕☕', '☕☕☕☕'),
        ('☕☕☕☕☕', '☕☕☕☕☕'),
    ])

    wifi_strength_rating = SelectField(u'Wifi Strength Rating', validators=[DataRequired()], choices=[
        ('✘', '✘'),
        ('💪', '💪'),
        ('💪💪', '💪💪'),
        ('💪💪💪', '💪💪💪'),
        ('💪💪💪💪', '💪💪💪💪'),
        ('💪💪💪💪💪', '💪💪💪💪💪'),
    ])

    power_socket_availability = SelectField(u'Power Socket Availability', validators=[DataRequired()], choices=[
        ('✘', '✘'),
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'),
    ])
    submit = SubmitField('Submit')


# Flask routes

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        add_entry_to_csv(form)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.DictReader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
