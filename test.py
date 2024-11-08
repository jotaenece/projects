# The given code takes a number from user input, passes it to the calc() function, and uses unpacking to get the returned values.

def calc(x):
    #your code goes here
    calc = (x*4, x**2)
    print(calc)
    return calc #return the tuple

side = int(input())
p, a = calc(side)


# side = int(input())
# p, a = calc(side)

print("Perimeter: " + str(p))
print("Area: " + str(a))