import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.listen()

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.onkeypress(player.move_forward, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)

    car_manager.move_cars()
    if car_manager.collision(player):
        game_is_on = False

    if player.ycor() >= 280:
        player.go_to_start()
        scoreboard.add_to_score()
        car_manager.increase_speed()

    screen.update()

scoreboard.game_over()
screen.exitonclick()
