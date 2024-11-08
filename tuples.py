"""
You are given a list of contacts, where each contact is represented by a tuple, with the name and age of the contact.

Complete the program to get a string as input,
search for the name in the list of contacts 
and output the age of the contact in the format presented below:

Sample Input
John

Sample Output 
John is 31
"""


contacts = [
    ('James', 42),
    ('Amy', 24),
    ('John', 31),
    ('Amanda', 63),
    ('Bob', 18)
]

x = str(input())

def search(y):
    found = False #seteamos variable a false, para ver si se encontró el contact
    for i in range(len(contacts)): # iteracion de todas las posiciones de la lista
        position = contacts[i] # primera posicion
        if y in position: # si lo que input está en la posicion buscada entonces print
            z = list(position)
            print(z[0] + " is " + str(z[1]))
            found = True
            break 
    if not found: 
        print("Not Found")
        
search(x)


