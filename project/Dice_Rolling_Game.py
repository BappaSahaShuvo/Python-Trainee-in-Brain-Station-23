import random

from numpy.random import choice

while True:
    choice = input("Do you want to roll again? (y/n): ").lower()
    if choice == "y":
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print(f"You rolled {dice1} and {dice2}")
    elif choice == "n":
        print("Thank you for playing!")
        break
    else:
        print("invalid choice.")
