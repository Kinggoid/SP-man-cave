list2 = [1, 8, 5, 1, 1, 2, 7, 2, 3, 9, 10, 3, 6, 5, 1, 7, 6, 4]


def count(list1, getal):
    y = 0

    for i in list1:
        if i == getal:
            y += 1
    return y


def opeenvolgendverschil(list1):
    list3 = []

    for i in range(0, len(list1) - 1):
        list3.append(abs(list1[i] - list1[i+1]))
    return max(list3)

def nullen(list1):
    nul = count(list1, 0)
    een = count(list1, 1)

    if een <= nul:
        return 'Er staan te veel nullen in de lijst'
    elif nul > 12:
        return 'Er mogen niet meer dan 12 nullen in de lijst staan'
    else:
        return 'Goed gedaan! De lijst voldoet aan alle condities'


print(count(list2, int(input('Getal: '))))
print(opeenvolgendverschil(list2))

list4 = [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]

print(nullen(list4))
