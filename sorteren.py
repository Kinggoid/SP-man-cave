eenlijst = [5, 4, 7, 8, 9, 5, 4, 2, 6, 3, 55, 44, 1, 6, 87, 4, 51, 25]


def sorteren(lst):
    tellen = 0
    while True:
        naamnietbelangrijk = 0
        for i in range(0, len(lst) - 1):
            tellen += 1
            if lst[i] > lst[i + 1]:
                naamnietbelangrijk += 1
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
        if naamnietbelangrijk == 0:
            break
    return lst


print(sorteren(eenlijst))