from turtle import Turtle

SPEED = 20

class Paddle(Turtle):
    def __init__(self, position, colour):
        super().__init__()
        self.position = position
        self.color(colour)
        self.paddle_init()
        self.speed("fastest")

    def go_up(self):
        self.goto(self.xcor(), (self.ycor() + SPEED))

    def go_down(self):
        self.goto(self.xcor(), (self.ycor() - SPEED))

    def paddle_init(self):
        self.penup()
        self.shape("square")
        self.shapesize(5, 1)
        self.goto(self.position)
4