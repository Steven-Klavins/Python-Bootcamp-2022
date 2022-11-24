from turtle import Turtle
import time

MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:

    def __init__(self, screen, number_of_sections=0, colour="white"):
        self.snake_sections = []
        self.screen = screen
        self.number_of_sections = number_of_sections
        self.colour = colour
        self.create_new_snake()
        self.head = self.snake_sections[0]

    def create_new_snake(self):
        if self.number_of_sections > 0:
            # Always add a head section regardless of number
            self.add_snake_section(setup=True)
            for _ in range(0, self.number_of_sections - 1):
                self.add_snake_section(setup=True)
            else:
                # Add head only
                self.add_snake_section(setup=True)

    def add_snake_section(self, position=(0, 0), setup=False):
        block = Turtle('square')
        block.penup()
        block.color(self.colour)
        if setup:
            block.setpos((len(self.snake_sections) - 1) * -20, 0)
        else:
            block.setpos(position)
        self.snake_sections.append(block)

    def extend(self):
        self.add_snake_section(self.snake_sections[-1].position())

    def move_forward(self):
        self.screen.update()
        time.sleep(0.1)
        for seg_num in range(len(self.snake_sections) - 1, 0, -1):
            new_x = self.snake_sections[seg_num - 1].xcor()
            new_y = self.snake_sections[seg_num - 1].ycor()
            self.snake_sections[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def reset(self):
        for section in self.snake_sections:
            section.goto(1000, 1000)
        self.snake_sections.clear()
        self.create_new_snake()
        self.head = self.snake_sections[0]


