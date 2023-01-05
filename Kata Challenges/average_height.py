student_heights = input("Input a list of student heights ").split()

length = len(student_heights)
total = sum([int(height) for height in student_heights])
average = round(total / length)

print(average)
