from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.canvas = Canvas()
        self.button_true = Button()
        self.button_false = Button()
        self.score_label = Label()
        # Order is important here, init and do setup , get next question, then run loop.
        self.question_text = ""
        self.quiz_window_init()
        self.get_next_question()
        self.window.mainloop()

    # ===== Window setup =====

    def quiz_window_init(self):

        # Window config
        self.window.config(padx=20, pady=20, bg=THEME_COLOR, height=500, width=420)

        # Canvas config
        self.canvas.config(width="300", height="250", bg="#fff", highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # Reassign empty sting to and actual canvas text object.
        self.question_text = self.canvas.create_text(150, 125, width=280, text="Some question text", fill="black",
                                                     font=("Arial", 20, "italic"))

        # Label config
        self.score_label.config(text="Score: 0", bg=THEME_COLOR, fg="#fff", font=("Ariel", 14, "bold"))
        self.score_label.grid(row=0, column=1)

        # true_img declared as global to preserved image.
        global true_img
        true_img = PhotoImage(file=r"images/true.png")
        self.button_true.config(image=true_img, command=self.check_answer_true)
        self.button_true.grid(row=2, column=0)

        # False config
        # false_img declared as global to preserved image.
        global false_img
        false_img = PhotoImage(file=r"images/false.png")
        self.button_false.grid(row=2, column=1)
        self.button_false.config(image=false_img, command=self.check_answer_false)

    def get_next_question(self):
        self.canvas.config(bg="#fff")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            question = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=question)
        else:
            # Disable buttons if the player has reached the end.
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.button_true.config(state="disabled")
            self.button_false.config(state="disabled")

    # Button methods

    def check_answer_true(self):
        is_correct = self.quiz.check_answer("True")
        self.give_feedback(is_correct)

    def check_answer_false(self):
        is_correct = self.quiz.check_answer("False")
        self.give_feedback(is_correct)

    # Flash red or green for right and wrong answers.

    def give_feedback(self, is_correct: bool):
        if is_correct:
            self.canvas.config(bg="#00FF00")
        else:
            self.canvas.config(bg="#FF0000")
        self.window.after(1000, self.get_next_question)
