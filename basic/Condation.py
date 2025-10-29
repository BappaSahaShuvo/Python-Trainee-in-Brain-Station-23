import random

a = int(input("Input the first number: "))
print("+ \n- \n* \n/")
c = input("Input the operation symbol: ")
b = int(input("Input the second number: "))
if c == "+":
    print(f"The sum of {a} and {b} is {a + b}")
elif c == "-":
    print(f"The difference of {a} and {b} is {a - b}")
elif c == "*":
    print(f"The product of {a} and {b} is {a * b}")
elif c == "/":
    try:
        print(f"The quotient of {a} and {b} is {a / b}")
    except ZeroDivisionError:
        print(f"The quotient of {a} and {b} is 0. So you can't divide by 0")
else:
    print("Invalid input")