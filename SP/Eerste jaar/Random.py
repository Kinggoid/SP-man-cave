import random


def randomgetal():
    welke = random.randint(1, 10)
    while True:
        getal = int(input('Kies een getal onder de 10: '))
        if getal == welke:
            print('Je hebt het geraden!: ')
            break

randomgetal()

