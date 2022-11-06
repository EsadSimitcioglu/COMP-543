from helper import letterFrequency, inv_uppercase, uppercase


def find_div(number):
    divisor_list = list()
    for i in range(2, number // 2):
        if number % i == 0:
            divisor_list.append(i)
    return divisor_list


def count_char(char, sentence):
    count_of_char = 0
    for i in sentence:
        if i == char:
            count_of_char += 1
    return count_of_char


def uppercase_val(char):
    return uppercase[char]


def val_uppercase(val):
    return inv_uppercase[val]


def decrypt(c, k):
    output = ''
    key_index = 0
    for x in c:
        if x == " ":
            output += " "
            continue
        output = output + val_uppercase((uppercase_val(x) - uppercase_val(k[key_index])) % 26)
        if key_index == len(k) - 1:
            key_index = 0
        else:
            key_index = key_index + 1

    return output


ciphertext = """Fwg atax: P’tx oh li hvabawl jwgvmjs, nw fw tfiapqz lziym, rqgv uuwfpxj wpbk jxlnlz fptf noqe wgw.
Qoifmowl P bdg mg xv qe ntlyk ba bnjh vcf ekghn
izl fq blidb eayz jgzbwx sqwm lgglbtqgy xlip.
Pho fvvs ktf C smf ur ecul ywndxlz uv mzcz xxivw?
Qomdmowl P bgzg, oblzqdxj C swas,
B kyl btm udujs dcbfm vn yg eazl, pqzx,
oblzq Q’ow mwmzb lg ghvk gxslz, emamwx apqu, wwmazagxv nomy bhlustk.”
Ghm qvv’f nbfx h vqe vgoubdg, pgh’a nuvw shvbtmk kbvzq.
Baam jqfg pafs ixetqm wcdanw svc.
Kwn’df dixs mzy ziym llllmfa, zjid wxl
bf nom eifw hlqspuglowall, loyv sztq cu btmlw mhuq phmmla. Kwn’df htiirk yul gx bf noqe kbls. Kwz’b agjl naz mzcuoe mekydpqzx: lblzq’a gg moqb nhj svc, fpxjy’z va zhsx.
Uwi basn fwg’dx ouzbql rgoy tunx zyym, uv mzcz ayied wvzzmk, qib’dq lxknywkmw an ldqzroblzq qg lbl eazev."""

ciphertext_uppercase = ciphertext.upper()
ciphertext_uppercase = ciphertext_uppercase.replace("\n", "")
ciphertext_uppercase = ciphertext_uppercase.replace(":", "")
ciphertext_uppercase = ciphertext_uppercase.replace("’", "")
ciphertext_uppercase = ciphertext_uppercase.replace(",", "")
ciphertext_uppercase = ciphertext_uppercase.replace(".", "")
ciphertext_uppercase = ciphertext_uppercase.replace("?", "")
ciphertext_uppercase = ciphertext_uppercase.replace("”", "")
ciphertext_uppercase_without_space = ciphertext_uppercase
ciphertext_uppercase = ciphertext_uppercase.replace(" ", "")

dict_of_tripgrah = {}
dict_of_div = {}
sorted_letter_Freq_dict = {}
key_choice_difference = {}
dict_of_ciphers = {}
key = str()

for elem in sorted(letterFrequency.items()):
    sorted_letter_Freq_dict[elem[0]] = elem[1]
letter_freq_list = [i for i in sorted_letter_Freq_dict.values()]
letter_list = [i for i in sorted_letter_Freq_dict.keys()]

for i in range(0, len(ciphertext_uppercase) - 2):
    three_word = ciphertext_uppercase[i] + ciphertext_uppercase[i + 1] + ciphertext_uppercase[i + 2]

    if not (three_word.isalpha()):
        continue

    last_index = i + 2

    if three_word in dict_of_tripgrah:
        continue
    else:
        for j in range(i + 1, len(ciphertext_uppercase) - 2):
            next_tripgrah = ciphertext_uppercase[j] + ciphertext_uppercase[j + 1] + ciphertext_uppercase[j + 2]

            if three_word == next_tripgrah:
                if three_word in dict_of_tripgrah:
                    dict_of_tripgrah[three_word] += [j + 2 - last_index]
                else:
                    dict_of_tripgrah[three_word] = [j + 2 - last_index]

for i in dict_of_tripgrah.values():
    for j in i:
        if j > 0:
            div_list = find_div(j)
            for div in div_list:
                if div in dict_of_div:
                    dict_of_div[div] += 1
                else:
                    dict_of_div[div] = 0

key_length = max(dict_of_div, key=dict_of_div.get)

for i in range(0, key_length):
    three_word = str()
    for index in range(i, len(ciphertext_uppercase), key_length):
        three_word += ciphertext_uppercase[index]
    dict_of_ciphers[i] = three_word

for cipher in dict_of_ciphers.values():
    print("*" * 30)
    char_occurance = list()
    min_result = 10000
    index_of_e = -1
    for index in range(65, 91):
        letter = chr(index)
        counter = count_char(letter, cipher)
        char_occurance.append(counter)

    for character in range(len(letter_freq_list)):
        char_occurance_index = 0
        result = 0
        temp_index_of_e = -1
        for index in range(65, 91):
            letter = chr(index)
            letChar = letter_list[(char_occurance_index + character) % 26]
            if letChar == "e":
                temp_index_of_e = index
            result += abs(abs(char_occurance[char_occurance_index]) - abs(
                letter_freq_list[(char_occurance_index + character) % 26]))
            print("Letter -> " + letter + " | Helper Letter -> " + letChar + " | Frequency from the cipher -> " + str(
                abs(char_occurance[char_occurance_index])) + " | Frequency from the helper -> " + str(
                abs(letter_freq_list[(char_occurance_index + character) % 26])) + " | Difference -> " + str(
                abs(char_occurance[char_occurance_index]) - abs(
                    letter_freq_list[(char_occurance_index + character) % 26])))
            char_occurance_index += 1

        print("*" * 30)
        if result < min_result:
            min_result = result
            index_of_e = temp_index_of_e

    key += (chr(index_of_e - 4))

print("Key is : " + key)
print("Plain Text : " + decrypt(ciphertext_uppercase_without_space, key))
