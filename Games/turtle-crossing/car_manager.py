from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.cars = []
        self.generate_cars()
        self.generate_cars()
        self.place_cars()
        self.speed = MOVE_INCREMENT

    def generate_cars(self):
        for colour in COLORS:
            car = Turtle()
            car.penup()
            car.color(colour)
            car.shape("square")
            car.shapesize(1, 2)
            self.cars.append(car)

    def place_cars(self):
        for car in self.cars:
            rand_x = random.randint(-240, 240)
            rand_y = random.randint(-240, 240)
            car.goto(rand_x, rand_y)

    def move_cars(self):
        for car in self.cars:
            car.setx(car.xcor() - self.speed)
            if car.xcor() < -320:
                new_y = random.randint(-240, 240)
                car.goto(320, new_y)

    def increase_speed(self):
        self.speed += 1

    def collision(self, player):
        for car in self.cars:
            if player.distance(car) < 20:
                return True
        return False
