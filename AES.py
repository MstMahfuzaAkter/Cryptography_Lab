S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,

    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,

    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
    0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,

    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
    0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,

    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,

    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
    0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,

    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
    0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,

    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,

    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
    0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,

    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
    0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,

    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,

    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
    0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,

    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
    0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,

    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,

    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
    0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,

    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
    0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

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


def char_to_hex(character):

    character = character.upper()

    if 'A' <= character <= 'Z':

        return ord(character) - ord('A')

    raise ValueError(
        "Only English letters A-Z are allowed."
    )


def prepare_input(text):

    text = text.upper()

    if len(text) < 16:

        text = text + 'Z' * (16 - len(text))

    elif len(text) > 16:

        text = text[:16]

    data = []

    for character in text:

        data.append(
            char_to_hex(character)
        )

    return data, text



def format_hex(data):

    return " ".join(
        f"{value:02X}"
        for value in data
    )



def print_matrix(state):

    for row in range(4):

        print(
            " ".join(
                f"{state[4 * column + row]:02X}"
                for column in range(4)
            )
        )


def add_round_key(state, round_key):

    result = []

    for i in range(16):

        result.append(
            state[i] ^ round_key[i]
        )

    return result


def sub_bytes(state):

    result = []

    for value in state:

        result.append(
            S_BOX[value]
        )

    return result



def shift_rows(state):

    result = [0] * 16

    for row in range(4):

        for column in range(4):

            new_column = (
                column + row
            ) % 4

            old_index = (
                4 * column + row
            )

            new_index = (
                4 * new_column + row
            )

            result[old_index] = (
                state[new_index]
            )

    return result



def xtime(value):

    if value & 0x80:

        return (
            ((value << 1) ^ 0x1B)
            & 0xFF
        )

    return (
        (value << 1)
        & 0xFF
    )


def gmul(a, b):

    result = 0

    while b:

        if b & 1:

            result ^= a

        a = xtime(a)

        b >>= 1

    return result



def mix_columns(state):

    result = [0] * 16

    for column in range(4):

        index = 4 * column

        a = state[index]
        b = state[index + 1]
        c = state[index + 2]
        d = state[index + 3]

        # Row 1
        result[index] = (
            gmul(a, 0x02)
            ^ gmul(b, 0x03)
            ^ c
            ^ d
        )

        # Row 2
        result[index + 1] = (
            a
            ^ gmul(b, 0x02)
            ^ gmul(c, 0x03)
            ^ d
        )

        # Row 3
        result[index + 2] = (
            a
            ^ b
            ^ gmul(c, 0x02)
            ^ gmul(d, 0x03)
        )

        # Row 4
        result[index + 3] = (
            gmul(a, 0x03)
            ^ b
            ^ c
            ^ gmul(d, 0x02)
        )

    return result



def rot_word(word):

    return (
        word[1:]
        + word[:1]
    )



def sub_word(word):

    result = []

    for value in word:

        result.append(
            S_BOX[value]
        )

    return result

def key_expansion(key):

    print("\n")
    print("                       KEY EXPANSION")
    print("=" * 70)

    words = []


    for i in range(0, 16, 4):

        words.append(
            key[i:i + 4]
        )

    print("\nOriginal Key Words:")

    for i in range(4):

        print(
            f"W{i} = "
            f"{format_hex(words[i])}"
        )

    print("\n")
    print("              ROUND 1 KEY GENERATION")
    print("=" * 70)

    print("\nW4 Generation")

    temp = words[3][:]

    print(
        f"\nW3 = {format_hex(temp)}"
    )

    # RotWord

    rotated = rot_word(temp)

    print(
        f"RotWord(W3): "
        f"{format_hex(temp)}"
        f" -> "
        f"{format_hex(rotated)}"
    )

    # SubWord

    substituted = sub_word(rotated)

    print("\nSubWord:")

    for i in range(4):

        print(
            f"S-Box[{rotated[i]:02X}] "
            f"= {substituted[i]:02X}"
        )

    temp = substituted

    # RCON

    print("\nRcon:")

    print(
        f"Rcon[1] = "
        f"{RCON[1]:02X}"
    )

    old = temp[0]

    temp[0] ^= RCON[1]

    print(
        f"{old:02X} XOR "
        f"{RCON[1]:02X} = "
        f"{temp[0]:02X}"
    )

    # XOR W0

    print("\nW4 XOR Calculation:")

    w4 = []

    for i in range(4):

        value = (
            words[0][i]
            ^ temp[i]
        )

        w4.append(value)

        print(
            f"{words[0][i]:02X} XOR "
            f"{temp[i]:02X} = "
            f"{value:02X}"
        )

    words.append(w4)

    print(
        f"\nW4 = {format_hex(w4)}"
    )


    print("\nW5 Generation")

    w5 = []

    for i in range(4):

        value = (
            words[1][i]
            ^ w4[i]
        )

        w5.append(value)

        print(
            f"{words[1][i]:02X} XOR "
            f"{w4[i]:02X} = "
            f"{value:02X}"
        )

    words.append(w5)

    print(
        f"W5 = {format_hex(w5)}"
    )

    print("\nW6 Generation")

    w6 = []

    for i in range(4):

        value = (
            words[2][i]
            ^ w5[i]
        )

        w6.append(value)

        print(
            f"{words[2][i]:02X} XOR "
            f"{w5[i]:02X} = "
            f"{value:02X}"
        )

    words.append(w6)

    print(
        f"W6 = {format_hex(w6)}"
    )


    print("\nW7 Generation")

    w7 = []

    for i in range(4):

        value = (
            words[3][i]
            ^ w6[i]
        )

        w7.append(value)

        print(
            f"{words[3][i]:02X} XOR "
            f"{w6[i]:02X} = "
            f"{value:02X}"
        )

    words.append(w7)

    print(
        f"W7 = {format_hex(w7)}"
    )

    print("\n")
    print("=" * 70)
    print("                  ROUND KEY 1")
    print("=" * 70)

    round_key_1 = (
        w4
        + w5
        + w6
        + w7
    )

    print(
        format_hex(round_key_1)
    )

    print("\nRound Key 1 Matrix:")

    print_matrix(round_key_1)


    for i in range(8, 44):

        temp = words[i - 1][:]

        if i % 4 == 0:

            temp = rot_word(temp)

            temp = sub_word(temp)

            temp[0] ^= RCON[i // 4]

        new_word = []

        for j in range(4):

            new_word.append(
                words[i - 4][j]
                ^ temp[j]
            )

        words.append(new_word)


    round_keys = []

    for round_number in range(11):

        round_key = []

        start = (
            round_number * 4
        )

        end = (
            start + 4
        )

        for word in words[start:end]:

            round_key.extend(word)

        round_keys.append(round_key)


    print("\n")
    print("                    ALL ROUND KEYS")
    print("=" * 70)

    for round_number in range(11):

        print(
            f"\nRound Key {round_number}:"
        )

        print(
            format_hex(
                round_keys[round_number]
            )
        )

    return round_keys



def full_round_1(state, round_key):

    print("\n")
    print("                         ROUND 1")
    print("=" * 70)

    # ========================================================
    # [1] SUB BYTES
    # ========================================================

    print("\n[1] SUB BYTES")
    print("-" * 60)

    print("\nBefore:")

    print_matrix(state)

    print("\nS-Box Substitution:")

    for i in range(16):

        print(
            f"{state[i]:02X}"
            f" -> "
            f"S-Box"
            f" -> "
            f"{S_BOX[state[i]]:02X}"
        )

    state = sub_bytes(state)

    print("\nAfter SubBytes:")

    print_matrix(state)


    print("\n[2] SHIFT ROWS")
    print("-" * 60)

    print("\nBefore:")

    print_matrix(state)

    print("\nOperation:")

    print(
        "Row 0 -> 0 position shift"
    )

    print(
        "Row 1 -> 1 position left"
    )

    print(
        "Row 2 -> 2 positions left"
    )

    print(
        "Row 3 -> 3 positions left"
    )

    state = shift_rows(state)

    print("\nAfter ShiftRows:")

    print_matrix(state)

    print("\n[3] MIX COLUMNS")
    print("-" * 60)

    print("\nBefore:")

    print_matrix(state)

    print("\nMixColumns Calculation:")

    for column in range(4):

        index = 4 * column

        a = state[index]
        b = state[index + 1]
        c = state[index + 2]
        d = state[index + 3]

        print(
            f"\nColumn {column + 1}: "
            f"{a:02X} {b:02X} "
            f"{c:02X} {d:02X}"
        )

        # Row 1

        a2 = gmul(a, 0x02)
        b3 = gmul(b, 0x03)

        r0 = (
            a2
            ^ b3
            ^ c
            ^ d
        )

        print(
            f"Row 1:"
        )

        print(
            f"02 x {a:02X} "
            f"XOR "
            f"03 x {b:02X} "
            f"XOR {c:02X} "
            f"XOR {d:02X}"
        )

        print(
            f"= {a2:02X} "
            f"XOR {b3:02X} "
            f"XOR {c:02X} "
            f"XOR {d:02X}"
        )

        print(
            f"= {r0:02X}"
        )

        # Row 2

        b2 = gmul(b, 0x02)
        c3 = gmul(c, 0x03)

        r1 = (
            a
            ^ b2
            ^ c3
            ^ d
        )

        print(
            f"\nRow 2:"
        )

        print(
            f"{a:02X} "
            f"XOR 02 x {b:02X} "
            f"XOR 03 x {c:02X} "
            f"XOR {d:02X}"
        )

        print(
            f"= {a:02X} "
            f"XOR {b2:02X} "
            f"XOR {c3:02X} "
            f"XOR {d:02X}"
        )

        print(
            f"= {r1:02X}"
        )

        # Row 3

        c2 = gmul(c, 0x02)
        d3 = gmul(d, 0x03)

        r2 = (
            a
            ^ b
            ^ c2
            ^ d3
        )

        print(
            f"\nRow 3:"
        )

        print(
            f"{a:02X} "
            f"XOR {b:02X} "
            f"XOR 02 x {c:02X} "
            f"XOR 03 x {d:02X}"
        )

        print(
            f"= {a:02X} "
            f"XOR {b:02X} "
            f"XOR {c2:02X} "
            f"XOR {d3:02X}"
        )

        print(
            f"= {r2:02X}"
        )

        # Row 4

        a3 = gmul(a, 0x03)
        d2 = gmul(d, 0x02)

        r3 = (
            a3
            ^ b
            ^ c
            ^ d2
        )

        print(
            f"\nRow 4:"
        )

        print(
            f"03 x {a:02X} "
            f"XOR {b:02X} "
            f"XOR {c:02X} "
            f"XOR 02 x {d:02X}"
        )

        print(
            f"= {a3:02X} "
            f"XOR {b:02X} "
            f"XOR {c:02X} "
            f"XOR {d2:02X}"
        )

        print(
            f"= {r3:02X}"
        )

    state = mix_columns(state)

    print("\nAfter MixColumns:")

    print_matrix(state)

    # ========================================================
    # [4] ADD ROUND KEY
    # ========================================================

    print("\n[4] ADD ROUND KEY")
    print("-" * 60)

    print("\nState:")

    print_matrix(state)

    print("\nRound Key 1:")

    print_matrix(round_key)

    print("\nXOR Calculation:")

    for i in range(16):

        result = (
            state[i]
            ^ round_key[i]
        )

        print(
            f"{state[i]:02X} XOR "
            f"{round_key[i]:02X} "
            f"= {result:02X}"
        )

    state = add_round_key(
        state,
        round_key
    )

    print("\nAfter AddRoundKey:")

    print_matrix(state)

    print(
        "\nRound 1 Output Hex:"
    )

    print(
        format_hex(state)
    )

    return state



def normal_round(state, round_key):

    state = sub_bytes(state)

    state = shift_rows(state)

    state = mix_columns(state)

    state = add_round_key(
        state,
        round_key
    )

    return state


def final_round(state, round_key):

    state = sub_bytes(state)

    state = shift_rows(state)

    state = add_round_key(
        state,
        round_key
    )

    return state


def aes_encrypt(text):


    plaintext_bytes, plaintext_final = (
        prepare_input(text)
    )

    key_bytes, key_final = (
        prepare_input(text)
    )


    print(
        f"\nOriginal Input:"
    )

    print(text)

    print(
        f"\nPlaintext after Z-padding:"
    )

    print(plaintext_final)

    print(
        "\nPlaintext Hex:"
    )

    print(
        format_hex(plaintext_bytes)
    )

    print(
        f"\nKey after Z-padding:"
    )

    print(key_final)

    print(
        "\nKey Hex:"
    )

    print(
        format_hex(key_bytes)
    )


    state = plaintext_bytes[:]

    print("\n")
    print("                    INITIAL STATE MATRIX")
    print("=" * 70)

    print_matrix(state)


    round_keys = key_expansion(
        key_bytes
    )


    print("\n")
    print("                    INITIAL ADD ROUND KEY")
    print("=" * 70)

    print("\nInitial State:")

    print_matrix(state)

    print("\nRound Key 0:")

    print_matrix(
        round_keys[0]
    )

    print("\nXOR:")

    for i in range(16):

        print(
            f"{state[i]:02X} XOR "
            f"{round_keys[0][i]:02X}"
            f" = "
            f"{state[i] ^ round_keys[0][i]:02X}"
        )

    state = add_round_key(
        state,
        round_keys[0]
    )

    print(
        "\nAfter Initial AddRoundKey:"
    )

    print_matrix(state)


    state = full_round_1(
        state,
        round_keys[1]
    )


    for round_number in range(2, 10):

        state = normal_round(
            state,
            round_keys[round_number]
        )

        print("\n")
        print("=" * 70)
        print(
            f"                    ROUND "
            f"{round_number} OUTPUT"
        )
        print("=" * 70)

        print("\nState Matrix:")

        print_matrix(state)

        print(
            "\nHex:"
        )

        print(
            format_hex(state)
        )


    state = final_round(
        state,
        round_keys[10]
    )

    print("\n")
    print("=" * 70)
    print("                    ROUND 10 OUTPUT")
    print("=" * 70)

    print(
        "\nSubBytes -> ShiftRows -> AddRoundKey"
    )

    print(
        "MixColumns -> SKIPPED"
    )

    print("\nState Matrix:")

    print_matrix(state)

    print(
        "\nHex:"
    )

    print(
        format_hex(state)
    )


    print("\n")
    print("=" * 70)
    print("                     FINAL CIPHERTEXT")
    print("=" * 70)

    print(
        "\nCiphertext Hex:"
    )

    print(
        format_hex(state)
    )

    print("\nFinal Ciphertext Matrix:")

    print_matrix(state)




while True:
    print("                    AES-128 ")
    print("=" * 70)

    print("1. Enter Plaintext")
    print("2. Exit")

    choice = input(
        "\nChoose an option (1/2): "
    ).strip()

    if choice == "2":
        print("              Program terminated.")
        print("=" * 70)

        break

    if choice != "1":

        print(
            "\n❌ Invalid option!"
        )

        print(
            "Please choose 1 or 2."
        )

        continue

    text = input(
        "\nEnter plaintext: "
    ).strip()


    if text == "":

        print(
            "\n❌ Error: Input cannot be empty."
        )

        continue


    text = text.upper()

    valid = True

    for character in text:

        if not (
            'A' <= character <= 'Z'
        ):

            valid = False

            break

    if not valid:

        print(
            "\n❌ Error: Only English "
            "letters A-Z are allowed."
        )

        continue

    print(
        "\nEncryption started..."
    )

    aes_encrypt(text)


    print("\n")
    print("              ENCRYPTION COMPLETED")
    print("=" * 70)