alph = 'abcdefghijklmnopqrstuvwxyz'
zin = input('Geef een zin: ')
rot = int(input('Geef een rotatienummer: '))
gevolg = ''

zin = zin.split(' ', 1)

for j in zin:
    for i in j:
        gevolg += alph[alph.index(i) + rot]
    gevolg += ' '


print(gevolg)