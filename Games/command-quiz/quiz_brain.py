class QuizBrain:
    # Init with starting values

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    # Return True until no questions are left

    def still_has_questions(self):
        if self.question_number < len(self.question_list):
            return True
        else:
            print("You have completed the quiz!")
            print(f"You final score was {self.score}/{self.question_number}")
            return False

    # Ask the next question     

    def next_question(self):
        current_question = self.question_list[self.question_number]
        answer = input(f"Q.{self.question_number + 1}: {current_question.text} (True/False)?: ")

        # Validate user's response

        if answer.lower() != "true" and answer.lower() != "false":
            print("Please respond either with 'True' or 'False.'")
        else:
            self.question_number += 1
            self.check_answer(current_question, answer)

    # Check answer, if user is correct add to their score    

    def check_answer(self, question, answer):
        if question.answer.lower() == answer.lower():
            print(f"Correct that was {question.answer.lower()}!")
            self.score += 1
        else:
            print(f"Incorrect that was {question.answer.lower()}!")
        print(f"Your current score is {self.score}/{self.question_number}\n")


