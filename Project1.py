price = 100000

while True:
    user_input = input("Has good credit? Write True or False: ").strip().lower()

    if user_input == "true":
        down_payment = price * 0.1
        print(f"Down payment: {down_payment}")
        break
    elif user_input == "false":
        down_payment = price * 0.2
        print(f"Down payment: {down_payment}")
        break
    else:
        print("Please enter True or False.")