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


def send_message(s):
    user_input = input("Your Reply: ")
    encrypted_message_str = str(encryption(user_input, s))
    encoded_message = encode_message(encrypted_message_str)

    with open("server.txt", "a") as file:
        file.write("******************************************")
        file.write("\nEncrypted Text: " + encoded_message)


def receive_message(encrypted_message, s):
    decrypted_message = decryption(encrypted_message, s)
    print("The Decryption of the Message is: " + decrypted_message)
    encoded_message = encode_message(decrypted_message)

    with open("server.txt", "a") as file:
        file.write("******************************************")
        file.write("\nDecrypted Message: " + decrypted_message + "\n")
        file.write("******************************************")


def encryption(user_input, s):
    encrypted_message = int.from_bytes(user_input.encode(), 'big') * s % q
    return encrypted_message


def decryption(encoded_message, s):
    encrypted_message = decode_message(encoded_message)
    decrypted_message = int(encrypted_message) * pow(s, q - 2, q) % q
    decrypted_message = decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big').decode()
    return decrypted_message


def check_message():
    lines = []
    encrypted_message_in_file = ""

    print("Waiting For Response...")

    while True:
        with open("server.txt", "r") as file:
            lines = file.readlines()
            for file_line in lines:
                if file_line[0:15] == "Encrypted Text:":
                    encrypted_message_in_file = file_line[16:]

        if encrypted_message_in_file != "":
            with open('server.txt', 'w') as f:
                for line in lines:
                    if not line.startswith('Encrypted Text:'):
                        f.write(line)
            break

        # Pause for 5 seconds
        time.sleep(5)

    return encrypted_message_in_file


def get_public_key():
    server = open("server.txt", "r+")

    public_key = ""
    for line in server.readlines():

        if line[0:10] == "Public Key":
            public_key = int(line[12:])

    return public_key


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

    h_encoded = encode_message(str(h))
    q_encoded = encode_message(str(q))
    g_encoded = encode_message(str(g))

    server.write("******************************************\n")
    server.write("H: " + h_encoded + "\n")
    server.write("Q: " + q_encoded + "\n")
    server.write("G: " + g_encoded + "\n")
    server.write("******************************************")

    server.close()


    while True:
        time.sleep(5)
        print("Deleting The Last Message")
        encrypted_message_in_file = check_message()
        public_key = get_public_key()
        s = pow(public_key, secret_key, q)
        receive_message(encrypted_message_in_file, s)
        send_message(s)

else:

    server.seek(0)

    h = ""
    h_encoded = ""
    q = ""
    q_encoded = ""
    g = ""
    g_encoded = ""

    for line in server.readlines():

        if line[0] == "H":
            h_encoded = line[3:]
        elif line[0] == "Q":
            q_encoded = line[3:]
        elif line[0] == "G":
            g_encoded = line[3:]



    h = int(decode_message(h_encoded))
    q = int(decode_message(q_encoded))
    g = int(decode_message(g_encoded))


    gen = cyclic_group_generator(q)

    k = next(gen(randprime(2, q)))
    while math.gcd(k, q) != 1:
        k = next(gen(randprime(2, q)))

    p = pow(g, k, q)
    s = pow(h, k, q)

    with open("server.txt", "a") as file:
        file.write("******************************************")
        file.write("\nPublic Key: " + str(p) + "\n")

    while True:
        send_message(s)
        time.sleep(5)
        print("Deleting The Last Message")
        encrypted_message_in_file = check_message()
        receive_message(encrypted_message_in_file, s)
