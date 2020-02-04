list2 = [1, 8, 5, 1, 1, 2, 7, 2, 3, 9, 10, 3, 6, 5, 1, 7, 6, 4]


def counte(list1):
    x = int(input('Getal: '))
    y = 0

    for i in list1:
        if i == x:
            y += 1
    return y


def opeenvolgendverschil(list1):
    list3 = []
    ll = 0

    for i in list1:
        ll += 1

    for i in range(0, ll - 1):
        list3 += abs(list1[i] - list1[i+1])
    return max(list3)


print(counte(list2))
print(opeenvolgendverschil(list2))
