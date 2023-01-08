import random

test_seed = int(input("Create a seed number: "))
random.seed(test_seed)

heads_or_tails = random.randint(0, 1)

if heads_or_tails == 1:
    print("Heads")
else:
    print("Tails")
