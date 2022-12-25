from Crypto.Random import random
from Crypto.Util.number import getPrime, GCD


def gcd(n1, n2):
    result = 1
    divisor = 2
    while divisor <= min(n1, n2):
        if n1 % divisor == 0 and n2 % divisor == 0:
            n1 /= divisor
            n2 /= divisor
            result *= divisor
            divisor = 2
            continue
        divisor += 1

    return result


# Choose a random prime q
q = getPrime(128)

# Choose a random generator g for the cyclic group F_q
g = 2
while gcd(g, q) != 1:
  g = random.randint(2, q - 1)

# The cyclic group F_q and the generator g have been chosen
print("Cyclic group: F_%d" % q)
print("Generator: %d" % g)