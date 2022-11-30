from turtle import Turtle, Screen
import random

colours = ["red", "orange", "yellow", "green", "blue", "purple"]
turtle_dictonary = {}
screen = Screen()
screen.setup(width=500, height=400)
MAX_SPEED = 15


def start(screen, max_speed):
    selected_tutrle = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a colour: ")
    generate_turtles()
    place_turtles()
    winner = start_race(max_speed)
    end_race(screen)
    determine_winner(selected_tutrle, winner)


def generate_turtles():
    for colour in colours:
        turtle = Turtle()
        turtle.shape("turtle")
        turtle.color(colour)
        turtle.penup()
        turtle_dictonary[colour] = turtle


def place_turtles():
    position = -100
    for turtle in turtle_dictonary:
        turtle_dictonary[turtle].goto(x=-230, y=position)
        position += 50


def start_race(max_speed):
    still_racing = True
    while still_racing:
        for turtle in turtle_dictonary:
            distance = random.randint(1, max_speed)
            if turtle_dictonary[turtle].xcor() + distance >= 240:
                turtle_dictonary[turtle].forward((240 - turtle_dictonary[turtle].xcor()))
                return turtle
            else:
                turtle_dictonary[turtle].forward(distance)


def end_race(screen):
    screen.bye()


def determine_winner(selected_turtle, winner):
    if selected_turtle == winner:
        print("The winner was " + winner + " you win!")
    else:
        print("The winner was " + winner + " you loose!")


start(screen, MAX_SPEED)
