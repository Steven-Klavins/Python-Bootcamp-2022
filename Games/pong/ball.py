from turtle import Turtle
import time

SPEED_INCREASE = 0.5
STARTING_SPEED = 10


class Ball(Turtle):
    def __init__(self, colour, screen):
        super().__init__()
        self.color(colour)
        self.ball_init()
        self.x_direction_value = STARTING_SPEED
        self.y_direction_value = STARTING_SPEED
        self.ball_speed = 10

    def ball_init(self):
        self.penup()
        self.shape("circle")

    def move(self):
        new_x = self.xcor() + self.x_direction_value
        new_y = self.ycor() + self.y_direction_value
        self.goto(new_x, new_y)
        time.sleep(0.08)

    def bounce_y(self):
        self.increase_speed()
        self.y_direction_value *= -1

    def bounce_x(self):
        self.increase_speed()
        self.x_direction_value *= -1

    def increase_speed(self):
        self.ball_speed += SPEED_INCREASE
        if self.x_direction_value < 0:
            self.x_direction_value = self.ball_speed * -1
        else:
            self.x_direction_value = self.ball_speed

        if self.y_direction_value < 0:
            self.y_direction_value = self.ball_speed * -1
        else:
            self.y_direction_value = self.ball_speed

    def reset_position(self):
        self.ball_speed = STARTING_SPEED
        self.goto(0, 0)
        self.bounce_x()
        time.sleep(1)
