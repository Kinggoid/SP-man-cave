file = open('stukjetekst.txt', 'r+')
nieuw = open('nieuwetekst.txt', 'r+')

lines = file.readlines()

for i in lines:
    if i[0] == '\n':
        lines.remove(i)

for i in lines:
    nieuw.write((i.strip() + '\n'))