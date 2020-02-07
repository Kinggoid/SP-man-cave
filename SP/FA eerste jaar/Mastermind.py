import random

kleuren = ['Rood', 'Groen', 'Geel', 'Blauw', 'Wit', 'Zwart']

antwoord = []

for i in range(0, 4):
    antwoord.append(random.choice(kleuren))

print(antwoord)


def guess():
    """In deze functie laten we de speler een antwoord geven."""
    gok = []
    for i in range(0, 4):
        gok.append(input('Voer een kleur in: '))

    for i in range(0, len(gok)):
        gok[i] = (gok[i].strip()).capitalize()

    print('Jouw gegeven volgorde is: ' + gok[0] + ' ' + gok[1] + ' ' + gok[2] + ' ' + gok[3])
    return gok


def test(antwoord):
    """Met deze functie willen we kijken of de speler het antwoord kan raden
     en geven we deze hints waarmee hij het daarna misschien zou kunnen raden."""
    PlekGoed = 0
    KleurGoed = 0
    kansen = 10

    while True:
        gok = guess()
        kansen -= 1 #Hier verliest de speler steeds één kans

        if gok == antwoord: #Als de speler het goed heeft
            print()
            return 'Gefeliciteerd, je hebt het geraden!'

        elif kansen == 0: #Als de speler geen levens meer heeft
            return 'Helaas, je hebt het niet kunnen raden binnen tien kansen.'

        else:
            for i in range(0, 4): #Dit laat zien hoeveel pionen er op de goede plekken zaten
                if antwoord[i] == gok[i]:
                    PlekGoed += 1
            KleurGoed -= PlekGoed
            for i in gok: #Dit laat zien hoeveel pionen op een andere plek behoren
                if i in antwoord:
                    KleurGoed += 1
            print()
            print(str(PlekGoed) + ' zat(en) goed en ' + str(KleurGoed) + ' zat(en) niet op de goede plek.')
            PlekGoed = 0 #Reset
            KleurGoed = 0 #Reset






print(test(antwoord))

