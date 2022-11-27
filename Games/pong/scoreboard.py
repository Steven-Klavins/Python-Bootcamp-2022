from turtle import Turtle

class ScoreBoard(Turtle):
    def __init__(self, colour):
        super().__init__()
        self.color(colour)
        self.l_score = 0
        self.r_score = 0
        self.penup()
        self.hideturtle()
        self.write_score()

    def write_score(self):
        self.clear()
        self.goto(-100, 200)
        self.write(self.l_score, align="center", font=("Courier", 80, "normal"))
        self.goto(100, 200)
        self.write(self.r_score, align="center", font=("Courier", 80, "normal"))

    def l_score_plus_one(self):
        self.l_score += 1
        self.write_score()

    def r_score_plus_one(self):
        self.r_score += 1
        self.write_score()
