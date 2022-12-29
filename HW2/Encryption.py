import math
import random
from ast import literal_eval
from sympy import gcd, randprime

def cyclic_group_generator(n):
    def generator(x):
        while True:
            x = x * x % n
            yield x
    return generator


user_input = input("Message : ")
file = open("server.txt","r+")

for line in file.readlines():

    if line[0] == "F":
        F = line[3:]
    elif line[0] == "H":
        h = int(line[3:])
    elif line[0] == "Q":
        q = int(line[3:])
    elif line[0] == "G":
        g = int(line[3:])

gen = cyclic_group_generator(q)

# 2. Alice encrypts the message using Bob’s public key:
# a. Alice chooses k from cyclic group F such that gcd(a, q) = 1
k = next(gen(randprime(2, q)))
while math.gcd(k, q) != 1:
    k = next(gen(randprime(2, q)))

# b. Alice computes p = gk and s = hk= gab
p = g ** k
s = h ** k

message_list = list()
for i in range(len(user_input)):
    message_list.append(user_input[i])

for i in range(len(message_list)):
    message_list[i] = s * ord(message_list[i])

# d. Alice publishes (p, M x s) = (gk , M x s)
ciphertext = (p, message_list)
encrypted_text = ""

for i in message_list:
    encrypted_text += str(i)


file.write("Public Key: " + p + " \n")
file.write("Encrypted Text: " + encrypted_text + "\n")
file.write("******************************************")
