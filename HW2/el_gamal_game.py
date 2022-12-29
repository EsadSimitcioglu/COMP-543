import base64
import math
import time
from sympy import gcd, randprime


# Generate a cyclic group Fq of size q
def cyclic_group_generator(n):
    def generator(x):
        while True:
            x = x * x % n
            yield x

    return generator


def encode_message(message):
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')

    return base64_message


def decode_message(encoded_message):
    base64_bytes = encoded_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('utf-8')

    return message


def send_message(server, s, p):
    user_input = input("Your Reply: ")
    encrypted_message_str = str(encryption(user_input, s))
    encoded_message = encode_message(encrypted_message_str)

    server.write("******************************************")
    server.write("\nPublic Key: " + str(p))
    server.write("\nEncrypted Text: " + encoded_message + "\n")
    server.write("******************************************")
    server.close()


def recieve_message(encrypted_message, server, s):
    decrypted_message = decryiption(encrypted_message, s)
    print(decrypted_message)
    encoded_message = encode_message(decrypted_message)

    server.write("******************************************")
    server.write("\nDecrypted Message: " + encoded_message + "\n")
    server.write("******************************************")


def encryption(user_input, s):
    encrypted_message = int.from_bytes(user_input.encode(), 'big') * s % q
    return encrypted_message


def decryiption(encoded_message, s):
    encrypted_message = decode_message(encoded_message)
    decrypted_message = int(encrypted_message) * pow(s, q - 2, q) % q
    decrypted_message = decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big').decode()
    return decrypted_message


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
    time.sleep(5)

    server = open("server.txt", "r+")

    public_key = ""
    encrypted_message = ""
    for line in server.readlines():

        if line[0:10] == "Public Key":
            public_key = int(line[12:])
        elif line[0:14] == "Encrypted Text":
            encrypted_message = line[16:]

    if encrypted_message != "":
        s = pow(public_key, secret_key, q)

        recieve_message(encrypted_message, server, s)
        send_message(server, s, h)


else:

    server.seek(0)

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

    k = next(gen(randprime(2, q)))
    while math.gcd(k, q) != 1:
        k = next(gen(randprime(2, q)))

    p = pow(g, k, q)
    s = pow(h, k, q)

    send_message(server, s, p)
    print("Waiting...")
    time.sleep(5)

    server = open("server.txt", "r+")

    encrypted_message = ""
    for line in server.readlines():

        if line[0:15] == "Encrypted Text:":
            encrypted_message = line[16:]

    recieve_message(encrypted_message, server, s)
