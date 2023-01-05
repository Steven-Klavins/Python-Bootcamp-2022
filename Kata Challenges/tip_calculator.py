print("Welcome to the tip calculator!")
total = float(input("What was the total bill? $"))
tip = int(input("How much tip would you like to give? 10, 12, or 15? "))
number_of_people = int(input("How many people to split the bill? "))

cost_per_person = round((total / number_of_people) * (1 + (tip / 100)), 2)

print(f"Each person should pay: ${cost_per_person:.2f}")
