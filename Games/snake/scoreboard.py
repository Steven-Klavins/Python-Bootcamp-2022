from turtle import Turtle
import time

ALIGNMENT = "center"
FONT = ('Arial', 16, 'normal')


class ScoreBoard(Turtle):
    def __init__(self, colour):
        super().__init__()
        self.color(colour)
        self.score = 0
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
            self.setup_board()
        except FileNotFoundError as e:
            with open("high_score.txt", "w") as file:
                file.write("0")
            self.high_score = 0
            self.setup_board()

    def setup_board(self):
        self.penup()
        self.sety(270)
        self.hideturtle()
        self.write(f"Score: {self.score} High score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def update_board(self):
        self.clear()
        self.write(f"Score: {self.score} High score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def add_to_score(self):
        self.score += 1
        self.update_board()

    def game_over(self):
        self.reset()
        self.sety(0)
        self.write("Game Over!", align=ALIGNMENT, font=FONT)
        time.sleep(2)
        self.clear()
        self.setup_board()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", mode="w") as file:
                file.write(str(self.score))
                self.setup_board()
        self.score = 0
