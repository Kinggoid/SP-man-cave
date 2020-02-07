def palindrome(tekst):
    omgedraaid = ''
    for i in tekst:
        omgedraaid = i + omgedraaid

    if omgedraaid == tekst:
        return 'Dit is een palindroom'
    else:
        return 'Dit is geen palindroom'


print(palindrome(input('Geef een woord: ')))


def palindrome2(tekst):
    stukjes = []
    for i in tekst:
        stukjes += i
    reverse = stukjes
    reverse.reverse()

    if stukjes == reverse:
        return 'Dit is een palindroom'
    else:
        return 'Dit is geen palindroom'


print(palindrome2(input('Geef een woord: ')))
