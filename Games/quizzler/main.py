from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

# Create a list of questions from the data module.

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# Create new instance of QuizBrain and pass it to the UI.
quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)
