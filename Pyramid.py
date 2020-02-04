groot = int(input('Hoe groot?: '))

for i in range(1, groot + 1):
    print(i * '*')
for i in range(1, groot + 1):
    print((groot - i) * '*')

x = 1
while x != groot + 1:
    print(x * '*')
    x += 1
while x != 0:
    print(x * '*')
    x -= 1
