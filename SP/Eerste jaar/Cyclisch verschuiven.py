ch = '10001011'


def verschuiven(bits, n):
    eerste, tweede = bits[0:n], bits[n:] #Hiermee split ik de bits in twee delen
    return tweede + eerste

print(verschuiven(ch, 4))