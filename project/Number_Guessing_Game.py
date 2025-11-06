import random
while True:
    guess = int(input("Guess a number between 1 and 100: "))
    computer = random.randint(1, 100)
    if guess == computer:
        print("You guessed right!")
    elif guess < computer:
        print("Your guess is too low.")
    elif guess > computer:
        print("Your guess is too high.")
    