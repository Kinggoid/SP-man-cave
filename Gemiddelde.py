def gemiddelde(lst):
    alles = 0
    for i in lst:
        alles += i
    return alles / len(lst)


def gemlisten(lst):
    alles = 0
    for i in lst:
        alles += gemiddelde(i)
    return alles / len(lst)

print(gemiddelde([5, 4, 7, 8, 9, 5, 4, 2, 6, 3, 55, 44, 1, 6, 87, 4, 51, 25]))
print(gemlisten([[8, 5, 9, 6, 7, 7], [8, 9, 7, 5, 8, 7, 9], [7, 8, 8, 5, 6, 4]]))