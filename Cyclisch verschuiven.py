ch = '10001011'


def verschuiven(bits, n):
    eerste, tweede = bits[0:n], bits[n:]
    return tweede + eerste

print(verschuiven(ch, 4))