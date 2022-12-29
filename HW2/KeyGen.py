# Import necessary libraries
import random
import math


# Define a class for the cyclic group Fq
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

# Alice's message
M = "Hello, Bob!"

# 2. Alice encrypts the message using Bob’s public key:
# a. Alice chooses k from cyclic group F such that gcd(a, q) = 1
k = random.choice(F)
while math.gcd(k, q) != 1:
    k = random.choice(F)

# b. Alice computes p = gk and s = hk= gab
p = g ** k
s = h ** k

message_list = list()
for i in range(len(M)):
    message_list.append(M[i])

for i in range(len(message_list)):
    message_list[i] = s * ord(message_list[i])

# d. Alice publishes (p, M x s) = (gk , M x s)
ciphertext = (p, message_list)

# 3. Bob decrypts the message:
# a. Bob calculates s’ = pb = gab
s_prime = p ** b

cipyer_list = list()
for i in range(len(message_list)):
    cipyer_list.append(chr(int(message_list[i] / s_prime)))

m_prime = ''.join(cipyer_list)
print("Decrypted message:", m_prime)
