from square_faaziz.square_formula import SquareFunction

a, b = map(int, input("Input a and b\n").split())

print("(a + b) ^ 2 is : ", SquareFunction().square_form(a, b))
