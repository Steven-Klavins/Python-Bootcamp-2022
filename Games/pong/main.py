from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard

# Screen Setup

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)
screen.listen()

# Paddle Setup

paddle_right = Paddle((350, 0), "white")
paddle_left = Paddle((-350, 0), "white")

# Paddle Controls

screen.onkeypress(paddle_right.go_up, "Up")
screen.onkeypress(paddle_right.go_down, "Down")

screen.onkeypress(paddle_left.go_up, "w")
screen.onkeypress(paddle_left.go_down, "s")

# Ball Setup

ball = Ball("white", screen)

# Scoreboard Setup

scoreboard = ScoreBoard("white")

# Start Game

game_is_on = True

while game_is_on:
    screen.update()
    ball.move()

    if ball.ycor() > (screen.canvheight - 20) or ball.ycor() < ((screen.canvheight * -1) + 20):
        ball.bounce_y()

    if ball.distance(paddle_right) < 50 and ball.xcor() > 320 or ball.distance(paddle_left) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    if ball.xcor() > 380:
        scoreboard.l_score_plus_one()
        ball.reset_position()

    if ball.xcor() < -380:
        scoreboard.r_score_plus_one()
        ball.reset_position()

screen.exitonclick()
