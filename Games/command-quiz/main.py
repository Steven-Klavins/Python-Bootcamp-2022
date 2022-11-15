from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_list = []

# Add questions from data to list

for question in question_data:
    question_list.append(Question(question["text"], question["answer"]))

# Init a new quiz brain

quiz_brain = QuizBrain(question_list)

# While the quiz brain still has questions proceed to the next

while quiz_brain.still_has_questions():
    quiz_brain.next_question()
