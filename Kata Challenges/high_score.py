student_scores = input("Input a list of student scores ").split()
student_scores = [int(score) for score in student_scores]

print(f"The highest score in the class is: {max(student_scores)}")
