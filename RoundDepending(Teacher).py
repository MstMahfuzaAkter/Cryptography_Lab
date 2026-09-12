# ============================================================
# COMBINED CIPHER TOOLKIT
# 1. DES (CUSTOM NUMBER OF ROUNDS)
# 2. CAESAR CIPHER
# 3. PLAYFAIR CIPHER
# Menu driven with a while loop for repeated input
# ============================================================

# ============================================================
# ---------------- DES (CONFIGURABLE ROUNDS) DATA/TABLES ------
# ============================================================

SHIFT_SCHEDULE = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

E = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,
    29,12,28,17,
    1,15,23,26,
    5,18,31,10,
    2,8,24,14,
    32,27,3,9,
    19,13,30,6,
    22,11,4,25
]

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

S_BOX = [

[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
],

[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
],

[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]


def hex_to_binary(hex_value):
    binary_value = ""
    for h in hex_value:
        binary_value += format(int(h, 16), "04b")
    return binary_value


def binary_to_hex(binary_value):
    result = ""
    for i in range(0, len(binary_value), 4):
        four_bits = binary_value[i:i + 4]
        result += format(int(four_bits, 2), "X")
    return result


def permute(data, table):
    result = ""
    for position in table:
        result += data[position - 1]
    return result


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def XOR(a, b):
    result = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result


def show(name, bits):
    print(name + " Binary :", bits)
    print(name + " HEX    :", binary_to_hex(bits))


def sbox_function(bits):
    result = ""
    print("\n---------------- S BOX ----------------")
    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]
        row = int(block[0] + block[5], 2)
        column = int(block[1:5], 2)
        value = S_BOX[i][row][column]
        output = format(value, "04b")
        print(
            "S" + str(i + 1),
            "Input =", block,
            "Row =", row,
            "Column =", column,
            "Value =", value,
            "Output =", output
        )
        result += output
    return result


def generate_key_for_round(C, D, round_no):

    shift_amount = SHIFT_SCHEDULE[round_no - 1]

    C = left_shift(C, shift_amount)
    D = left_shift(D, shift_amount)

    CD = C + D
    Kn = permute(CD, PC2)

    print("\n---- Round", round_no, "Key Generation ----")
    print("Shift Amount :", shift_amount)
    show("C" + str(round_no), C)
    show("D" + str(round_no), D)
    show("K" + str(round_no), Kn)

    return C, D, Kn


def run_des_rounds():

    print("\n================================================")
    print("             DES (CUSTOM NUMBER OF ROUNDS)")
    print("================================================")

    plaintext = input("\nEnter 16 HEX characters: ").upper()

    if len(plaintext) != 16:
        print("\nERROR!")
        print("You must enter exactly 16 hexadecimal characters.")
        return

    for ch in plaintext:
        if ch not in "0123456789ABCDEF":
            print("\nERROR!")
            print("Only hexadecimal characters are allowed.")
            return

    num_rounds_input = input("How many rounds do you want to see (1-16)? ")

    if not num_rounds_input.isdigit():
        print("\nERROR!")
        print("Please enter a valid number.")
        return

    num_rounds = int(num_rounds_input)

    if num_rounds < 1 or num_rounds > 16:
        print("\nERROR!")
        print("Number of rounds must be between 1 and 16.")
        return

    print("\n================================================")
    print("1. PLAINTEXT")
    print("================================================")
    print("Plaintext HEX :", plaintext)
    plaintext_binary = hex_to_binary(plaintext)
    show("Plaintext", plaintext_binary)

    print("\n================================================")
    print("2. KEY (SAME AS PLAINTEXT)")
    print("================================================")
    key = plaintext
    print("Key HEX :", key)
    key_binary = hex_to_binary(key)
    show("Key", key_binary)

    print("\n================================================")
    print("3. PC-1")
    print("================================================")
    pc1_result = permute(key_binary, PC1)
    show("PC-1", pc1_result)

    C = pc1_result[:28]
    D = pc1_result[28:]

    print("\n================================================")
    print("4. INITIAL PERMUTATION")
    print("================================================")
    IP_result = permute(plaintext_binary, IP)
    show("IP", IP_result)

    L = IP_result[:32]
    R = IP_result[32:]

    show("L0", L)
    show("R0", R)

    print("\n================================================")
    print("5. KEY SCHEDULE + ROUNDS")
    print("================================================")

    for round_no in range(1, num_rounds + 1):

        C, D, Kn = generate_key_for_round(C, D, round_no)

        print("\n================================================")
        print("              ROUND", round_no)
        print("================================================")

        show("L" + str(round_no - 1), L)
        show("R" + str(round_no - 1), R)

        expanded_R = permute(R, E)
        show("Expanded R" + str(round_no - 1), expanded_R)

        xor_result = XOR(expanded_R, Kn)
        show("XOR Result", xor_result)

        sbox_result = sbox_function(xor_result)
        print("\nS BOX TOTAL OUTPUT:")
        show("S-Box", sbox_result)

        pbox_result = permute(sbox_result, P)
        show("P-Box", pbox_result)

        L_new = R
        R_new = XOR(L, pbox_result)

        show("L" + str(round_no), L_new)
        show("R" + str(round_no), R_new)

        L, R = L_new, R_new

    print("\n================================================")
    print("              FINAL OUTPUT AFTER ROUND", num_rounds)
    print("================================================")
    round_output = L + R
    show("Round " + str(num_rounds) + " Output", round_output)

    print("\n================================================")
    print("              COMPLETED")
    print("================================================")



# ============================================================
# ---------------- CAESAR CIPHER ------------------------------
# ============================================================

def run_caesar_cipher():

    text = input("Enter text: ")
    shift = int(input("Enter shift value: "))

    encrypted = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            encrypted += char

    print("Encrypted Text:", encrypted)

    decrypted = ""
    for char in encrypted:
        if char.isalpha():
            if char.isupper():
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char

    print("Decrypted Text:", decrypted)


# ============================================================
# ---------------- PLAYFAIR CIPHER -----------------------------
# ============================================================

def create_matrix(key):
    key = key.upper().replace("J", "I")

    matrix = ""
    for ch in key:
        if ch.isalpha() and ch not in matrix:
            matrix += ch

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in matrix:
            matrix += ch

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def find_position(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j


def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join(ch for ch in text if ch.isalpha())

    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + "X"
            i += 1

    return result


def playfair_encrypt(text, matrix):
    result = ""
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1 + 1) % 5]
            result += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 + 1) % 5][c1]
            result += matrix[(r2 + 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result


def playfair_decrypt(text, matrix):
    result = ""
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1 - 1) % 5]
            result += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 - 1) % 5][c1]
            result += matrix[(r2 - 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result


def run_playfair_cipher():

    key = input("Enter key: ")
    plaintext = input("Enter plaintext: ")

    matrix = create_matrix(key)

    print("\nPlayfair Matrix:")
    for row in matrix:
        print(" ".join(row))

    prepared = prepare_text(plaintext)
    print("\nPrepared Text:", prepared)

    encrypted = playfair_encrypt(prepared, matrix)
    print("Encrypted Text:", encrypted)

    decrypted = playfair_decrypt(encrypted, matrix)
    print("Decrypted Text:", decrypted)


# ============================================================
# ---------------- MAIN MENU (WHILE LOOP) ----------------------
# ============================================================

def main():

    while True:

        print("\n================================================")
        print("             CIPHER TOOLKIT MENU")
        print("================================================")
        print("1. DES (Choose Number of Rounds)")
        print("2. Caesar Cipher")
        print("3. Playfair Cipher")
        print("4. Exit")
        print("================================================")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            run_des_rounds()
        elif choice == "2":
            run_caesar_cipher()
        elif choice == "3":
            run_playfair_cipher()
        elif choice == "4":
            print("\nExiting program. Bye!")
            break
        else:
            print("\nInvalid choice! Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()