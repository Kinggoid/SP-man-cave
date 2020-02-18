import random


def code():
    """In deze functie laten we de speler zijn code invoeren."""
    orde = []
    for i in range(0, 4):
        orde.append(input('Voer een Cijfer in: '))

    for i in range(0, len(orde)):
        orde[i] = (orde[i].strip()).capitalize()

    print('Jouw gegeven volgorde is: ' + orde[0] + ' ' + orde[1] + ' ' + orde[2] + ' ' + orde[3])
    return orde


def test(antwoord):
    """Met deze functie willen we kijken of de speler het antwoord kan raden
     en geven we deze hints waarmee hij het daarna misschien zou kunnen raden."""
    kansen = 10

    while kansen > 0:
        gok = code()

        kansen -= 1 #Hier verliest de speler steeds één kans

        if gok == antwoord: #Als de speler het goed heeft
            return '\n' + 'Gefeliciteerd, je hebt het geraden!'

        else:
            punten = feedback(gok, antwoord)
            print('\n' + str(punten[0]) + ' zat(en) goed en ' + str(punten[1]) + ' zat(en) niet op de goede plek.')
    return 'Helaas, je hebt het niet kunnen raden binnen tien kansen.'


def feedback(gok, antwoord):
    """Met deze functie willen we de feedback geven voor Mastermind."""
    PlekGoed = 0
    CijferGoed = 0

    for i in range(0, 4):  # Dit laat zien hoeveel pionen er op de goede plekken zaten
        if antwoord[i] == gok[i]:
            PlekGoed += 1

    for i in gok:  # Dit laat zien hoeveel pionen op een andere plek behoren
        if i in antwoord:
            CijferGoed += 1

    CijferGoed -= PlekGoed
    return [PlekGoed, CijferGoed]


def algoritme(gamemode):
    """In deze algoritme staan twee algorimes, je kan één van
    deze twee functies gebruiken om codes te raden met Mastermind"""

    lst = {
        '[0, 0]': 0, '[0, 1]': 0, '[0, 2]': 0, '[0, 3]': 0, '[0, 4]': 0, '[1, 1]': 0, '[1, 2]': 0,
        '[1, 3]': 0, '[2, 1]': 0, '[2, 2]': 0, '[3, 0]': 0, '[1, 0]': 0, '[2, 0]': 0, '[4, 0]': 0
    }

    groot = [0, '']
    if gamemode == 'hard':
        groot[0] = 520

    for i in alles:
        for u in alles:
            for j in lst:
                if str(feedback(u, i)) == j:
                    lst[j] = lst[j] + 1

        if gamemode == 'hard':
            n = 0
            totaal = len(alles)
            hier = 0

            for p in lst:
                n += lst[p]
                hier += (lst[p] ** 2) / totaal

            if hier < groot[0]:
                groot[0] = hier
                groot[1] = i

            for p in lst:
                lst[p] = 0

        else:
            samen = 0

            for p in lst:
                if int(p[1]) + int(p[4]) >= 3:
                    samen += lst[p]

            if samen / 14 > groot[0]:
                groot[0] = samen / 14
                groot[1] = i

            for i in lst:
                lst[i] = 0
    return groot[1]



def comp(gamemode):
    tussenlijst = []
    beurten = 10
    antwoord = code()

    while beurten > 0:
        hints = []

        if len(alles) == 0:
            return 'Er is geen gok meer mogelijk, de feedback moet ergens verkeerd zijn gegaan.'

        if gamemode == 'easy':
            gok = random.choice(alles)
        else:
            gok = algoritme(gamemode)

        print('\nDe computer raadt: ' + gok[0] + ', ' + gok[1] + ', ' + gok[2] + ', ' + gok[3] + '\n')

        if gok == antwoord:
            return 'Ah jammer, de computer heeft gewonnen. Probeer het nog eens.'

        while True:
            try:
                goed = int(input('Hoeveel pionen zitten op de goede plek?: '))
                bijnagoed = int(input('Hoeveel pionen zitten in de code maar zitten niet op de goede plek?: '))
                hints.append(goed)
                hints.append(bijnagoed)
                break
            except:
                print('Oeps, je deed iets verkeerd. Probeer antwoord te geven als zo: 1')

        beurten -= 1

        for i in alles:
            if feedback(i, gok) == hints:
                tussenlijst.append(i)

        alles.clear()
        for i in tussenlijst:
            alles.append(i)

        tussenlijst.clear()
    return 'De computer had jouw antwoord niet binnen 10 keer kunnen raden, jij wint!'


lijst = ['A', 'B', 'C', 'D', 'E', 'F']

antwoord = []

print("Welkom! Leuk dat je Mastermind wilt gaan spelen.")

while True:
    wie = input('Typ "raden" als je wilt raden en "computer" als je wilt dat de computer raadt: ')
    if wie == 'raden' or wie == 'Raden':
        for i in range(0, 4):
            antwoord.append(random.choice(lijst))
        print('Nu is het de tijd om de code te raden.\n')
        print(test(['F', 'B', 'B', 'E']))
        break

    elif wie == 'computer' or wie == 'Computer':
        while True:
            mode = input('Wil je de gamemode zetten op easy, medium of hard?: ')
            if mode == 'easy' or mode == 'medium' or mode == 'hard':
                break
            else:
                print('Dit is niet één van de opties, probeer het nog eens.')

        alles = []
        for i in lijst:
            for j in lijst:
                for u in lijst:
                    for g in lijst:
                        alles.append([i, j, u, g])

        print('Tijd om jouw code te maken.\nGeef een code van vier cijfers, je hebt de keuze uit: A, B, C, D, E, F.')

        print(comp(mode))
        break

    else:
        print('Dit was niet één van de twee opties, probeer het nog eens.', '\n')
