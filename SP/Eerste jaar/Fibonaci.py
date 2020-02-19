def fibonaci(een, twee, n):
    antwoord = een + twee
    if n <= 1:
        return 0
    elif n == 2:
        return antwoord
    else:
        return fibonaci(twee, antwoord, n-1)


print(fibonaci(0, 1, int(input('Input getal: '))))
