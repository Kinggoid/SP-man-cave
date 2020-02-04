def tekstcheck():
    string1 = input('Geef een zinnetje lullo: ')
    string2 = input('Als je niet een lullo wilt zijn moet je me nog een zinnetje geven: ')
    x = 0

    while True:
        if x + 1 > len(string1) or x + 1 > len(string2):
            print('Je zinnetje verschilt voor het eerst op index ' + str(x + 1) + '... lullo')
            break
        elif string1[x] == string2[x]:
            x += 1
        else:
            print('Je zinnetje verschilt voor het eerst op index ' + str(x + 1) + '... lullo')
            break

tekstcheck()