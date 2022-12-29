import math
import random
import sys
sys.set_int_max_str_digits(100000)


class Fq:
    def __init__(self, q):
        self.q = q
        self.elements = [i for i in range(q)]

    def __mul__(self, other):
        return (self.q * other.q) % self.q

    def __pow__(self, exponent):
        return (self.q ** exponent) % self.q




# 1. Bob generates public and private keys:
# a. Bob chooses a large number q and a cyclic group Fq
q = random.randint(1000, 10000)
Fq = Fq(q)

# b. Bob chooses a random generator g for Fq and an element a such that gcd(b,q) = 1
g = random.choice(Fq.elements)
b = random.choice(Fq.elements)
while math.gcd(b, q) != 1:
    b = random.choice(Fq.elements)

# c. Bob computes h = gb
h = g ** b

# d. Bob publishes F, h, q and g, retains b as private key
F = Fq.elements
public_key = (F, h, q, g)
private_key = b

file = open("server.txt","a")
file.write("******************************************\n")
file.write("F: " + str(F) + "\n")
file.write("H: " + str(h) + "\n")
file.write("Q: " + str(q) + "\n")
file.write("G: " + str(g) + "\n")
file.write("******************************************")
