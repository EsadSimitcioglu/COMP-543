ciphertext = "kyivv izexj wfi kyv vcmve-bzexj leuvi kyv jbp, jvmve wfi kyv unriwcfiuj ze kyvzi yrccj fw jkfev, ezev wfi dfikrc dve uffdvu kf uzv, fev wfi kyv urib cfiu fe yzj urib kyifev; ze kyv creu fw dfiufi nyviv kyv jyrufnj czv. fev izex kf ilcv kyvd rcc, fev izex kf wzeu kyvd, fev izex kf sizex kyvd rcc, reu ze kyv uribevjj szeu kyvd; ze kyv creu fw dfiufi nyviv kyv jyrufnj czv."

key = 16

for key in range(1,25):
    plaintext_prime = str()
    for element in ciphertext:
        if 122 >= ord(element) >= 97:
            shifter = ord(element)
            if shifter+key > 122:
                shifter += key
                shifter -= 122
                shifter += 96
            else:
                shifter += key
            plaintext_prime += chr(shifter)
        else:
            plaintext_prime += " "

    print("Key : " + str(key))
    print("Plaintext : " + plaintext_prime)
    print("************")
