def tekstcheck():
    string1 = input('Schrijf een zinnetje: ')
    string2 = input('Schrijf nog een zinnetje: ')
    x = 0

    while True:
        if x + 1 > len(string1) or x + 1 > len(string2):
            print('Je zinnetje verschilt voor het eerst op index ' + str(x + 1))
            break
        elif string1[x] == string2[x]:
            x += 1
        else:
            print('Je zinnetje verschilt voor het eerst op index ' + str(x + 1))
            break

tekstcheck()
