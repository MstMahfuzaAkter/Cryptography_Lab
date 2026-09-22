# ============================================================
#                 DES + AES COMPLETE PROGRAM
# ============================================================
#
# DES:
#   HEX INPUT
#   HEX -> BINARY
#   INITIAL PERMUTATION
#   KEY GENERATION
#   16 ROUNDS
#   FINAL SWAP
#   FINAL PERMUTATION
#
# AES:
#   A = 00
#   B = 01
#   C = 02
#   ...
#   Y = 18
#   Z = 19
#
#   If input < 16 characters:
#       Add Z
#
#   If input > 16 characters:
#       Take first 16 characters
#
#   KEY = PLAINTEXT
# ============================================================


# ============================================================
#                         DES TABLES
# ============================================================

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


FP = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
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


SHIFT = [
    1,1,2,2,2,2,2,2,
    1,2,2,2,2,2,2,1
]


# ============================================================
#                         DES S-BOX
# ============================================================

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


# ============================================================
#                    DES HEX -> BINARY
# ============================================================

def hex_to_bits(text):

    bits = ""

    i = 0

    while i < len(text):

        bits += format(
            int(text[i], 16),
            "04b"
        )

        i += 1

    return bits


# ============================================================
#                    BINARY -> HEX
# ============================================================

def bits_to_hex(bits):

    result = ""

    i = 0

    while i < len(bits):

        result += format(
            int(bits[i:i+4], 2),
            "X"
        )

        i += 4

    return result


# ============================================================
#                  SHOW HEX -> BINARY
# ============================================================

def show_binary(bits):

    print("\n==============================================")
    print("                 HEX TO BINARY")
    print("==============================================")

    i = 0

    while i < len(bits):

        print(
            "Bits {:02d}-{:02d} = {}".format(
                i + 1,
                i + 4,
                bits[i:i+4]
            )
        )

        i += 4

    print("\nComplete Binary:")

    i = 0

    while i < len(bits):

        print(
            bits[i:i+8],
            end=" "
        )

        i += 8

    print()


# ============================================================
#                       PERMUTE
# ============================================================

def permute(bits, table):

    result = ""

    i = 0

    while i < len(table):

        result += bits[
            table[i] - 1
        ]

        i += 1

    return result


# ============================================================
#                          XOR
# ============================================================

def xor_bits(a, b):

    result = ""

    i = 0

    while i < len(a):

        if a[i] == b[i]:

            result += "0"

        else:

            result += "1"

        i += 1

    return result


# ============================================================
#                       LEFT SHIFT
# ============================================================

def left_shift(bits, n):

    return bits[n:] + bits[:n]


# ============================================================
#                 DES INITIAL PERMUTATION
# ============================================================

def show_ip(bits):

    print("\n==============================================")
    print("             INITIAL PERMUTATION")
    print("==============================================")

    result = ""

    i = 0

    while i < 64:

        position = IP[i]

        bit = bits[position - 1]

        print(
            "IP[{:02d}] <- Input[{:02d}] = {}".format(
                i + 1,
                position,
                bit
            )
        )

        result += bit

        i += 1

    print("\nAfter IP Binary:")

    i = 0

    while i < 64:

        print(
            result[i:i+8],
            end=" "
        )

        i += 8

    print()

    print(
        "\nAfter IP HEX =",
        bits_to_hex(result)
    )

    return result


# ============================================================
#                 DES FINAL PERMUTATION
# ============================================================

def show_fp(bits):

    print("\n==============================================")
    print("             FINAL PERMUTATION")
    print("==============================================")

    result = ""

    i = 0

    while i < 64:

        position = FP[i]

        bit = bits[position - 1]

        print(
            "FP[{:02d}] <- Input[{:02d}] = {}".format(
                i + 1,
                position,
                bit
            )
        )

        result += bit

        i += 1

    print(
        "\nFinal Cipher Binary:"
    )

    i = 0

    while i < 64:

        print(
            result[i:i+8],
            end=" "
        )

        i += 8

    print()

    print(
        "\nFinal Cipher HEX =",
        bits_to_hex(result)
    )

    return result


# ============================================================
#                  DES KEY GENERATION
# ============================================================

def generate_des_keys(key_bits):

    print("\n==============================================")
    print("              DES KEY GENERATION")
    print("==============================================")

    pc1 = permute(
        key_bits,
        PC1
    )

    print(
        "\nAfter PC-1 =",
        bits_to_hex(pc1)
    )

    C = pc1[:28]

    D = pc1[28:]

    print(
        "C0 =",
        bits_to_hex(C)
    )

    print(
        "D0 =",
        bits_to_hex(D)
    )

    keys = []

    round_no = 1

    while round_no <= 16:

        C = left_shift(
            C,
            SHIFT[round_no - 1]
        )

        D = left_shift(
            D,
            SHIFT[round_no - 1]
        )

        combined = C + D

        K = permute(
            combined,
            PC2
        )

        keys.append(K)

        print(
            "\nRound {}:".format(
                round_no
            )
        )

        print(
            "C{} = {}".format(
                round_no,
                bits_to_hex(C)
            )
        )

        print(
            "D{} = {}".format(
                round_no,
                bits_to_hex(D)
            )

        )

        print(
            "K{} = {}".format(
                round_no,
                bits_to_hex(K)
            )
        )

        round_no += 1

    return keys


# ============================================================
#                       DES S-BOX
# ============================================================

def des_sbox(bits):

    result = ""

    print("\n---------- S-BOX ----------")

    box = 0

    while box < 8:

        six = bits[
            box * 6:
            (box + 1) * 6
        ]

        row = int(
            six[0] + six[5],
            2
        )

        column = int(
            six[1:5],
            2
        )

        value = S_BOX[
            box
        ][
            row
        ][
            column
        ]

        four = format(
            value,
            "04b"
        )

        print(
            "S{}: {} -> Row={} Column={} -> {} -> {}".format(
                box + 1,
                six,
                row,
                column,
                value,
                four
            )
        )

        result += four

        box += 1

    return result


# ============================================================
#                         DES ROUND
# ============================================================

def des_round(
    L,
    R,
    key,
    round_no
):

    print("\n==============================================")
    print(
        "                  DES ROUND",
        round_no
    )
    print("==============================================")

    print(
        "L{} = {}".format(
            round_no - 1,
            bits_to_hex(L)
        )
    )

    print(
        "R{} = {}".format(
            round_no - 1,
            bits_to_hex(R)
        )
    )

    print(
        "K{} = {}".format(
            round_no,
            bits_to_hex(key)
        )
    )

    # --------------------------------------------------------
    # EXPANSION
    # --------------------------------------------------------

    expanded = permute(
        R,
        E
    )

    print(
        "\n1. Expansion E(R) =",
        bits_to_hex(expanded)
    )

    # --------------------------------------------------------
    # XOR
    # --------------------------------------------------------

    mixed = xor_bits(
        expanded,
        key
    )

    print(
        "2. XOR with K =",
        bits_to_hex(mixed)
    )

    # --------------------------------------------------------
    # S BOX
    # --------------------------------------------------------

    s_result = des_sbox(
        mixed
    )

    print(
        "\nS-Box output =",
        bits_to_hex(s_result)
    )

    # --------------------------------------------------------
    # P BOX
    # --------------------------------------------------------

    p_result = permute(
        s_result,
        P
    )

    print(
        "\n4. P-Box =",
        bits_to_hex(p_result)
    )

    # --------------------------------------------------------
    # XOR WITH L
    # --------------------------------------------------------

    new_R = xor_bits(
        L,
        p_result
    )

    new_L = R

    print(
        "\n5. New R = L XOR P(S-box)"
    )

    print(
        "R{} = {}".format(
            round_no,
            bits_to_hex(new_R)
        )
    )

    print(
        "\n6. Swap:"
    )

    print(
        "L{} = {}".format(
            round_no,
            bits_to_hex(new_L)
        )
    )

    print(
        "R{} = {}".format(
            round_no,
            bits_to_hex(new_R)
        )
    )

    return new_L, new_R


# ============================================================
#                       DES ENCRYPTION
# ============================================================

def des_encrypt():

    print("\n\n")
    print("################################################")
    print("#                    DES                       #")
    print("#              KEY = PLAINTEXT                #")
    print("################################################")

    plaintext = input(
        "\nEnter 16-digit hexadecimal plaintext: "
    ).upper()

    if len(plaintext) != 16:

        print(
            "\nERROR: Exactly 16 hexadecimal digits required."
        )

        return

    i = 0

    while i < len(plaintext):

        if plaintext[i] not in "0123456789ABCDEF":

            print(
                "\nERROR: Invalid hexadecimal character."
            )

            return

        i += 1

    # KEY = PLAINTEXT

    key = plaintext

    print(
        "\nPlaintext =",
        plaintext
    )

    print(
        "Key       =",
        key
    )

    # --------------------------------------------------------
    # HEX -> BINARY
    # --------------------------------------------------------

    plaintext_bits = hex_to_bits(
        plaintext
    )

    key_bits = hex_to_bits(
        key
    )

    show_binary(
        plaintext_bits
    )

    # --------------------------------------------------------
    # INITIAL PERMUTATION
    # --------------------------------------------------------

    ip = show_ip(
        plaintext_bits
    )

    L = ip[:32]

    R = ip[32:]

    print(
        "\nL0 =",
        bits_to_hex(L)
    )

    print(
        "R0 =",
        bits_to_hex(R)
    )

    # --------------------------------------------------------
    # KEY GENERATION
    # --------------------------------------------------------

    keys = generate_des_keys(
        key_bits
    )

    # --------------------------------------------------------
    # 16 ROUNDS
    # --------------------------------------------------------

    round_no = 1

    while round_no <= 16:

        L, R = des_round(
            L,
            R,
            keys[round_no - 1],
            round_no
        )

        round_no += 1

    print("\n==============================================")
    print("              AFTER ROUND 16")
    print("==============================================")

    print(
        "L16 =",
        bits_to_hex(L)
    )

    print(
        "R16 =",
        bits_to_hex(R)
    )

    # --------------------------------------------------------
    # FINAL SWAP
    # --------------------------------------------------------

    combined = R + L

    print(
        "\nAfter Final Swap =",
        bits_to_hex(combined)
    )

    # --------------------------------------------------------
    # FINAL PERMUTATION
    # --------------------------------------------------------

    cipher_bits = show_fp(
        combined
    )

    ciphertext = bits_to_hex(
        cipher_bits
    )

    print("\n")
    print("################################################")
    print(
        "# DES CIPHERTEXT =",
        ciphertext
    )
    print("################################################")


# ============================================================
#                         AES S-BOX
# ============================================================

AES_SBOX = [

0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,
0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,

0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,
0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,

0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,
0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,

0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,
0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,

0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,
0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,

0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,
0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,

0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,
0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,

0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,
0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,

0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,
0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,

0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,
0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,

0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,
0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,

0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,
0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,

0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,
0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,

0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,
0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,

0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,
0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,

0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,
0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]


# ============================================================
#                         RCON
# ============================================================

RCON = [
    0x00,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36
]


# ============================================================
#             AES LETTER -> HEX VALUE
# ============================================================

def letter_to_value(ch):

    # A = 00
    # B = 01
    # ...
    # Z = 19

    return ord(ch) - ord("A")


# ============================================================
#              SHOW AES LETTER CONVERSION
# ============================================================

def show_aes_conversion(text):

    print("\n==============================================")
    print("          AES LETTER -> HEX VALUE")
    print("==============================================")

    i = 0

    while i < len(text):

        value = letter_to_value(
            text[i]
        )

        print(
            "{} = {:02X}".format(
                text[i],
                value
            )
        )

        i += 1

    print(
        "\nComplete:"
    )

    i = 0

    while i < len(text):

        value = letter_to_value(
            text[i]
        )

        print(
            "{:02X}".format(
                value
            ),
            end=" "
        )

        i += 1

    print()


# ============================================================
#                   AES TEXT -> STATE
# ============================================================

def text_to_aes_state(text):

    state = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    index = 0

    col = 0

    while col < 4:

        row = 0

        while row < 4:

            state[col][row] = \
                letter_to_value(
                    text[index]
                )

            index += 1

            row += 1

        col += 1

    return state


# ============================================================
#                    PRINT AES STATE
# ============================================================

def print_aes_state(state, title):

    print("\n" + title)

    row = 0

    while row < 4:

        print(
            "{:02X} {:02X} {:02X} {:02X}".format(
                state[0][row],
                state[1][row],
                state[2][row],
                state[3][row]
            )
        )

        row += 1


# ============================================================
#                   AES ADD ROUND KEY
# ============================================================

def aes_add_round_key(state, key):

    result = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    col = 0

    while col < 4:

        row = 0

        while row < 4:

            result[col][row] = \
                state[col][row] ^ \
                key[col][row]

            row += 1

        col += 1

    return result


# ============================================================
#                       AES SUB BYTES
# ============================================================

def aes_sub_bytes(state):

    result = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    col = 0

    while col < 4:

        row = 0

        while row < 4:

            value = state[col][row]

            result[col][row] = \
                AES_SBOX[value]

            row += 1

        col += 1

    return result


# ============================================================
#                       AES SHIFT ROWS
# ============================================================

def aes_shift_rows(state):

    result = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    row = 0

    while row < 4:

        col = 0

        while col < 4:

            result[col][row] = \
                state[
                    (col + row) % 4
                ][row]

            col += 1

        row += 1

    return result


# ============================================================
#                   AES GALOIS MULTIPLICATION
# ============================================================

def aes_gmul(a, b):

    result = 0

    i = 0

    while i < 8:

        if b & 1:

            result = result ^ a

        high_bit = a & 0x80

        a = (
            a << 1
        ) & 0xFF

        if high_bit:

            a = a ^ 0x1B

        b = b >> 1

        i += 1

    return result


# ============================================================
#                       AES MIX COLUMNS
# ============================================================

def aes_mix_columns(state):

    result = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    col = 0

    while col < 4:

        a0 = state[col][0]
        a1 = state[col][1]
        a2 = state[col][2]
        a3 = state[col][3]

        result[col][0] = \
            aes_gmul(a0, 2) ^ \
            aes_gmul(a1, 3) ^ \
            a2 ^ a3

        result[col][1] = \
            a0 ^ \
            aes_gmul(a1, 2) ^ \
            aes_gmul(a2, 3) ^ \
            a3

        result[col][2] = \
            a0 ^ a1 ^ \
            aes_gmul(a2, 2) ^ \
            aes_gmul(a3, 3)

        result[col][3] = \
            aes_gmul(a0, 3) ^ \
            a1 ^ a2 ^ \
            aes_gmul(a3, 2)

        col += 1

    return result


# ============================================================
#                       AES ROT WORD
# ============================================================

def aes_rot_word(word):

    result = [
        word[1],
        word[2],
        word[3],
        word[0]
    ]

    return result


# ============================================================
#                       AES SUB WORD
# ============================================================

def aes_sub_word(word):

    result = []

    i = 0

    while i < 4:

        result.append(
            AES_SBOX[
                word[i]
            ]
        )

        i += 1

    return result


# ============================================================
#                    AES KEY EXPANSION
# ============================================================

def aes_key_expansion(key):

    print("\n==============================================")
    print("                AES KEY EXPANSION")
    print("==============================================")

    words = []

    # --------------------------------------------------------
    # W0 - W3
    # --------------------------------------------------------

    i = 0

    while i < 4:

        word = [
            key[i][0],
            key[i][1],
            key[i][2],
            key[i][3]
        ]

        words.append(
            word
        )

        print(
            "W{} = {}".format(
                i,
                " ".join(
                    format(
                        x,
                        "02X"
                    )
                    for x in word
                )
            )
        )

        i += 1

    # --------------------------------------------------------
    # W4 - W43
    # --------------------------------------------------------

    i = 4

    while i < 44:

        temp = words[
            i - 1
        ][:]

        if i % 4 == 0:

            print(
                "\nW{}:".format(
                    i
                )
            )

            # RotWord

            temp = aes_rot_word(
                temp
            )

            print(
                "RotWord =",
                " ".join(
                    format(
                        x,
                        "02X"
                    )
                    for x in temp
                )
            )

            # SubWord

            temp = aes_sub_word(
                temp
            )

            print(
                "SubWord =",
                " ".join(
                    format(
                        x,
                        "02X"
                    )
                    for x in temp
                )
            )

            # RCON

            temp[0] = \
                temp[0] ^ \
                RCON[
                    i // 4
                ]

            print(
                "Rcon XOR =",
                " ".join(
                    format(
                        x,
                        "02X"
                    )
                    for x in temp
                )
            )

        new_word = []

        j = 0

        while j < 4:

            new_word.append(
                words[i - 4][j] ^
                temp[j]
            )

            j += 1

        words.append(
            new_word
        )

        print(
            "W{} = {}".format(
                i,
                " ".join(
                    format(
                        x,
                        "02X"
                    )
                    for x in new_word
                )
            )
        )

        i += 1

    # --------------------------------------------------------
    # ROUND KEYS
    # --------------------------------------------------------

    round_keys = []

    round_no = 0

    while round_no <= 10:

        round_key = [
            words[
                round_no * 4
            ],
            words[
                round_no * 4 + 1
            ],
            words[
                round_no * 4 + 2
            ],
            words[
                round_no * 4 + 3
            ]
        ]

        round_keys.append(
            round_key
        )

        print_aes_state(
            round_key,
            "ROUND KEY " +
            str(round_no) +
            ":"
        )

        round_no += 1

    return round_keys


# ============================================================
#                       AES ENCRYPTION
# ============================================================

def aes_encrypt():

    print("\n\n")
    print("################################################")
    print("#                   AES-128                    #")
    print("#               KEY = PLAINTEXT               #")
    print("#               A=00 ... Z=19                 #")
    print("################################################")

    plaintext = input(
        "\nEnter plaintext: "
    ).upper()

    # --------------------------------------------------------
    # REMOVE SPACES
    # --------------------------------------------------------

    plaintext = plaintext.replace(
        " ",
        ""
    )

    # --------------------------------------------------------
    # CHECK A-Z
    # --------------------------------------------------------

    i = 0

    while i < len(plaintext):

        if plaintext[i] < "A" or \
           plaintext[i] > "Z":

            print(
                "\nERROR: Only A-Z allowed."
            )

            return

        i += 1

    # --------------------------------------------------------
    # PADDING WITH Z
    # --------------------------------------------------------

    if len(plaintext) < 16:

        print(
            "\nPlaintext has less than 16 characters."
        )

        while len(plaintext) < 16:

            plaintext += "Z"

        print(
            "After Z padding =",
            plaintext
        )

    # --------------------------------------------------------
    # TRUNCATE
    # --------------------------------------------------------

    elif len(plaintext) > 16:

        print(
            "\nPlaintext has more than 16 characters."
        )

        plaintext = plaintext[:16]

        print(
            "First 16 characters =",
            plaintext
        )

    else:

        print(
            "\nPlaintext already has 16 characters."
        )

    # --------------------------------------------------------
    # KEY = PLAINTEXT
    # --------------------------------------------------------

    key_text = plaintext

    print(
        "\nPlaintext =",
        plaintext
    )

    print(
        "Key       =",
        key_text
    )

    # --------------------------------------------------------
    # LETTER -> HEX
    # --------------------------------------------------------

    show_aes_conversion(
        plaintext
    )

    # --------------------------------------------------------
    # CREATE STATE
    # --------------------------------------------------------

    state = text_to_aes_state(
        plaintext
    )

    key = text_to_aes_state(
        key_text
    )

    print_aes_state(
        state,
        "\nINITIAL PLAINTEXT STATE:"
    )

    print_aes_state(
        key,
        "\nINITIAL KEY STATE:"
    )

    # --------------------------------------------------------
    # KEY EXPANSION
    # --------------------------------------------------------

    round_keys = aes_key_expansion(
        key
    )

    # --------------------------------------------------------
    # INITIAL ADD ROUND KEY
    # --------------------------------------------------------

    print("\n==============================================")
    print("             INITIAL ADD ROUND KEY")
    print("==============================================")

    state = aes_add_round_key(
        state,
        round_keys[0]
    )

    print_aes_state(
        state,
        "After Initial AddRoundKey:"
    )

    # --------------------------------------------------------
    # ROUND 1 - 9
    # --------------------------------------------------------

    round_no = 1

    while round_no <= 9:

        print("\n==============================================")
        print(
            "                  AES ROUND",
            round_no
        )
        print("==============================================")

        # ----------------------------------------------------
        # SUB BYTES
        # ----------------------------------------------------

        state = aes_sub_bytes(
            state
        )

        print_aes_state(
            state,
            "1. After SubBytes:"
        )

        # ----------------------------------------------------
        # SHIFT ROWS
        # ----------------------------------------------------

        state = aes_shift_rows(
            state
        )

        print_aes_state(
            state,
            "2. After ShiftRows:"
        )

        # ----------------------------------------------------
        # MIX COLUMNS
        # ----------------------------------------------------

        state = aes_mix_columns(
            state
        )

        print_aes_state(
            state,
            "3. After MixColumns:"
        )

        # ----------------------------------------------------
        # ADD ROUND KEY
        # ----------------------------------------------------

        state = aes_add_round_key(
            state,
            round_keys[round_no]
        )

        print_aes_state(
            state,
            "4. After AddRoundKey:"
        )

        round_no += 1

    # --------------------------------------------------------
    # ROUND 10
    # --------------------------------------------------------

    print("\n==============================================")
    print("                  AES ROUND 10")
    print("==============================================")

    # SUB BYTES

    state = aes_sub_bytes(
        state
    )

    print_aes_state(
        state,
        "1. After SubBytes:"
    )

    # SHIFT ROWS

    state = aes_shift_rows(
        state
    )

    print_aes_state(
        state,
        "2. After ShiftRows:"
    )

    # NO MIX COLUMNS

    print(
        "\n3. MixColumns = SKIPPED"
    )

    # ADD ROUND KEY

    state = aes_add_round_key(
        state,
        round_keys[10]
    )

    print_aes_state(
        state,
        "3. After AddRoundKey:"
    )

    # --------------------------------------------------------
    # CIPHERTEXT
    # --------------------------------------------------------

    ciphertext = ""

    col = 0

    while col < 4:

        row = 0

        while row < 4:

            ciphertext += format(
                state[col][row],
                "02X"
            )

            row += 1

        col += 1

    print("\n################################################")
    print(
        "# AES CIPHERTEXT =",
        ciphertext
    )
    print("################################################")


# ============================================================
#                         MAIN MENU
# ============================================================

while True:

    print("\n\n")
    print("################################################")
    print("#             DES + AES PROGRAM               #")
    print("################################################")

    print("\n1. DES")
    print("2. AES")
    print("3. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        des_encrypt()

    elif choice == "2":

        aes_encrypt()

    elif choice == "3":

        print(
            "\nProgram ended."
        )

        break

    else:

        print(
            "\nInvalid choice."
        )
