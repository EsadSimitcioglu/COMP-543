import math
import time

from cryptography.hazmat.primitives.asymmetric import rsa

from sympy import gcd, randprime

# Generate a cyclic group Fq of size q
def cyclic_group_generator(n):
    def generator(x):
        while True:
            x = x * x % n
            yield x

    return generator


server = open("server.txt", "r+")

if len(server.readlines()) == 0:
    # Generate a 1024-bit prime number q
    q = randprime(2 ** 1023, 2 ** 1024)

    # Create the generator function for the cyclic group of size q
    gen = cyclic_group_generator(q)

    # Generate a 1024-bit prime number q
    q = randprime(2 ** 1023, 2 ** 1024)

    # Choose a random generator g for Fq
    g = next(gen(randprime(2, q)))

    # Choose an element a such that gcd(a, q) = 1
    secret_key = randprime(2, q)
    while gcd(secret_key, q) != 1:
        secret_key = randprime(2, q)

    # Compute h = g^a
    h = pow(g, secret_key, q)

    # Publish Fq, h, q, and g, retain a as private key
    print("Public key:")
    print("h:", h)
    print("q:", q)
    print("g:", g)
    print("Private key:")
    print("a:", secret_key)

    server.write("******************************************\n")
    server.write("H: " + str(h) + "\n")
    server.write("Q: " + str(q) + "\n")
    server.write("G: " + str(g) + "\n")
    server.write("******************************************")

    server.close()

    print("Waiting...")
    time.sleep(15)

    server = open("server.txt", "r+")

    public_key = ""
    encrypted_text = ""
    for line in server.readlines():

        if line[0:10] == "Public Key":
            public_key = int(line[12:])
        elif line[0:14] == "Encrypted Text":
            encrypted_text = line[16:]

    if encrypted_text != "":

        # 3. Bob decrypts the message:
        # a. Bob calculates s’ = pb = gab
        s_prime = pow(public_key, secret_key, q)

        cipyer_list = list()
        for i in range(len(encrypted_text)):
            if encrypted_text[i] != "\n":
                cipyer_list.append(chr(int(int(encrypted_text[i]) / s_prime)))

        m_prime = ''.join(cipyer_list)
        print("Decrypted message:", m_prime)


else:

    server.seek(0)
    user_input = input("Your Message: ")

    h = ""
    q = ""
    g = ""

    for line in server.readlines():

        if line[0] == "H":
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
    p = pow(g, k, q)
    s = pow(h, k, q)

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

    server.write("\nPublic Key: " + str(p) + " \n")
    server.write("Encrypted Text: " + encrypted_text + "\n")
    server.write("******************************************")
