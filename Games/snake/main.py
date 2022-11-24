from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import ScoreBoard

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake")
screen.tracer(0)

scoreboard = ScoreBoard("white")
scoreboard.update_board()

snake = Snake(screen, 2, "white")
food = Food()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    snake.move_forward()

    # Detect collision with food
    if snake.head.distance(food) < 15:
        snake.extend()
        scoreboard.add_to_score()
        food.refresh()

    # Detect collision wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        scoreboard.game_over()
        snake.reset()

    # Detect collision tail
    for section in snake.snake_sections[1:]:
        if snake.head.distance(section) < 10:
            scoreboard.game_over()

screen.exitonclick()
scoreboard.add_to_score(1)
scoreboard.update_board()
