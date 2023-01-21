import os
import random
from flask import Flask

app = Flask(__name__)
answer = random.randint(0, 9)


# Decorator for adding images conditionally
def image_decorator(function):
    def wrapper(*args, **kwargs):
        if kwargs['number'] == answer:
            count_img_path = os.path.join('static', 'correct.gif')
        elif kwargs['number'] < answer:
            count_img_path = os.path.join('static', 'low.gif')
        else:
            count_img_path = os.path.join('static', 'high.gif')
        return f'{function(kwargs["number"])} <img src="{count_img_path}">'

    return wrapper


def reassign_answer():
    global answer
    answer = random.randint(0, 9)


@app.route('/')
def guess_page():
    count_img_path = os.path.join('static', 'count.gif')
    return f'<h1>Guess a number between 0 and 9</h1> <img src="{count_img_path}">'


@app.route('/<int:number>')
@image_decorator
def answer_page(number):
    if number == answer:
        # Reassign the number if it's found.
        reassign_answer()
        return '<h1 style="color:green">You found me!</h1>'
    elif number > answer:
        return '<h1 style="color:purple">Too high, try again!</h1>'
    else:
        return '<h1 style="color:red">Too low, try again!</h1>'
