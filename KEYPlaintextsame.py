"""
EASY DES + AES (step by step)
=============================
Menu:  1 = DES   2 = AES   3 = Exit

DES : you type ONE 16-digit HEX value (64 bits). It is used as BOTH the plaintext and the key.
AES : you type ONE text (up to 16 characters, the rest is filled with Z). It is used as BOTH the plaintext and the key.
"""

# =====================================================================
#                              D E S
# =====================================================================

# Initial Permutation: shuffles the 64 input bits
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation: the reverse of IP
FP = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

# Expansion: 32 bits -> 48 bits (some bits are repeated)
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

# P-Box: shuffles the 32-bit S-Box output
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# Key schedule tables
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]      # 64 -> 56 bits

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]           # 56 -> 48 bits

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]        # left shifts per round

# 8 S-Boxes: each takes 6 bits and gives 4 bits (4 rows x 16 columns)
SBOX = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]


# ---------- small helper functions ----------
def permute(bits, table):
    """Rearrange bits using a table (table numbers start from 1)."""
    return "".join(bits[i - 1] for i in table)


def xor(a, b):
    """XOR of two bit-strings."""
    return "".join("0" if x == y else "1" for x, y in zip(a, b))


def bits_to_hex(bits):
    return format(int(bits, 2), "0%dX" % (len(bits) // 4))


def hex_to_bits(h):
    """16 hex digits -> 64 bits."""
    return bin(int(h, 16))[2:].zfill(len(h) * 4)


def text_to_bits(text):
    """Text -> bits (8 bits per character)."""
    return "".join(format(b, "08b") for b in text.encode("utf-8"))


def spaced(bits, n):
    """Print bits in groups of n so they are easy to read."""
    return " ".join(bits[i:i + n] for i in range(0, len(bits), n))


# ---------- DES key generation ----------
def des_make_keys(key_bits, show):
    """64-bit key -> sixteen 48-bit round keys."""
    k = permute(key_bits, PC1)            # PC-1: 64 -> 56 bits
    left, right = k[:28], k[28:]          # split into two halves
    keys = []
    i = 0
    while i < 16:
        s = SHIFTS[i]
        left = left[s:] + left[:s]        # circular left shift
        right = right[s:] + right[:s]
        rk = permute(left + right, PC2)   # PC-2: 56 -> 48 bits
        keys.append(rk)
        if show:
            print("  Key %2d = %s" % (i + 1, spaced(rk, 6)))
        i += 1
    return keys


# ---------- DES main algorithm ----------
def des_run(block_bits, keys, show):
    """Runs DES on one 64-bit block. Decrypt = same code with reversed keys."""
    bits = permute(block_bits, IP)                       # Initial Permutation
    left, right = bits[:32], bits[32:]
    print("\n[Initial Permutation]  L0 = %s  R0 = %s" % (bits_to_hex(left), bits_to_hex(right)))

    r = 0
    while r < 16:                                        # 16 rounds
        expanded = permute(right, E)                     # Expansion 32 -> 48
        mixed = xor(expanded, keys[r])                   # XOR with round key

        sbox_out = ""
        i = 0
        while i < 8:                                     # S-Box: 6 bits -> 4 bits
            chunk = mixed[i * 6:(i + 1) * 6]
            row = int(chunk[0] + chunk[5], 2)            # first + last bit
            col = int(chunk[1:5], 2)                     # middle 4 bits
            sbox_out += format(SBOX[i][row * 16 + col], "04b")
            i += 1

        pbox = permute(sbox_out, P)                      # P-Box
        new_right = xor(left, pbox)                      # XOR with old left
        left, right = right, new_right                   # swap halves

        if show:
            print("\n[Round %d]" % (r + 1))
            print("  Expansion : " + spaced(expanded, 6))
            print("  XOR (key) : " + spaced(mixed, 6))
            print("  S-Box     : " + spaced(sbox_out, 4))
            print("  P-Box     : " + spaced(pbox, 4))
        print("  Round %2d -> L = %s  R = %s" % (r + 1, bits_to_hex(left), bits_to_hex(right)))
        r += 1

    result = permute(right + left, FP)                   # swap + Final Permutation
    print("\n[Final Permutation] done")
    return result


def get_text(prompt, size, last=""):
    """Keeps asking until the text is exactly `size` bytes long. Enter = reuse `last`."""
    while True:
        s = input(prompt)
        if s == "" and last:
            return last
        if len(s.encode("utf-8")) == size:
            return s
        print("  Please type exactly %d characters (you typed %d)." % (size, len(s.encode("utf-8"))))


def get_text_z(prompt, size, last=""):
    """Up to `size` characters. If shorter, the rest is filled with 'Z'. Enter = reuse `last`."""
    while True:
        s = input(prompt)
        if s == "" and last:
            return last
        n = len(s.encode("utf-8"))
        if 1 <= n <= size:
            return s + "Z" * (size - n)
        print("  Please type 1 to %d characters (you typed %d)." % (size, n))


def get_hex(prompt, size, last):
    """Keeps asking until a valid hex string of `size` digits is given."""
    while True:
        s = input(prompt).strip()
        if s == "" and last:
            return last
        try:
            if len(s) == size:
                int(s, 16)
                return s.upper()
        except ValueError:
            pass
        print("  Please type exactly %d hex digits (0-9, A-F)." % size)


def des_menu():
    last_cipher = ""
    while True:
        print("\n------ DES MENU ------")
        print("1. Encrypt   (one 16-digit hex value = plaintext AND key)")
        print("2. Decrypt")
        print("3. Back")
        ch = input("Choice: ").strip()

        if ch == "1":
            value = get_hex("Enter 16 hex digits (plaintext = key) [Enter = 133457799BBCDFF1]: ",
                            16, "133457799BBCDFF1")
            show = input("Show every step of every round? (y/n): ").lower() == "y"
            bits = hex_to_bits(value)                    # same 64 bits used as plaintext AND key
            print("\nPlaintext = Key = %s" % value)
            print("\n[Key Generation]")
            keys = des_make_keys(bits, True)
            cipher = bits_to_hex(des_run(bits, keys, show))
            last_cipher = cipher
            print("\n>>> CIPHERTEXT (hex):", cipher)

        elif ch == "2":
            cipher = get_hex("Ciphertext (16 hex digits%s): " %
                             (", Enter = last one" if last_cipher else ""), 16, last_cipher)
            key = get_hex("Key (the same 16 hex digits): ", 16, "")
            show = input("Show every step of every round? (y/n): ").lower() == "y"
            keys = des_make_keys(hex_to_bits(key), False)
            keys.reverse()                               # decrypt = keys in reverse order
            plain_bits = des_run(hex_to_bits(cipher), keys, show)
            print("\n>>> PLAINTEXT (hex):", bits_to_hex(plain_bits))

        elif ch == "3":
            break
        else:
            print("  Please choose 1, 2 or 3.")


# =====================================================================
#                              A E S
# =====================================================================
def gmul(a, b):
    """Multiplication in GF(2^8), the special math AES uses."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def make_sbox():
    """Builds the AES S-Box: inverse in GF(2^8), then a fixed bit mixing."""
    sbox = []
    for x in range(256):
        inv = 0
        if x != 0:
            inv = 1
            while gmul(x, inv) != 1:
                inv += 1
        s = inv
        for k in range(1, 5):
            s ^= ((inv << k) | (inv >> (8 - k))) & 0xFF
        sbox.append(s ^ 0x63)
    return sbox


SBOX_AES = make_sbox()
INV_SBOX_AES = [0] * 256
for i in range(256):
    INV_SBOX_AES[SBOX_AES[i]] = i

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def show_state(title, s):
    """Print the 16 bytes as a 4x4 table (filled column by column)."""
    print("  " + title)
    for r in range(4):
        print("     " + " ".join("%02X" % s[r + 4 * c] for c in range(4)))


def key_expansion(key):
    """16-byte key -> 11 round keys (44 words of 4 bytes)."""
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    i = 4
    while i < 44:
        t = w[i - 1][:]
        if i % 4 == 0:
            t = t[1:] + t[:1]                       # RotWord
            t = [SBOX_AES[b] for b in t]            # SubWord
            t[0] ^= RCON[i // 4 - 1]                # Rcon
        w.append([w[i - 4][j] ^ t[j] for j in range(4)])
        i += 1
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]


def add_round_key(s, k):
    return [a ^ b for a, b in zip(s, k)]            # XOR state with round key


def sub_bytes(s):
    return [SBOX_AES[b] for b in s]                 # replace each byte using the S-Box


def inv_sub_bytes(s):
    return [INV_SBOX_AES[b] for b in s]


def shift_rows(s):
    """Row r is rotated left by r positions."""
    return [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def inv_shift_rows(s):
    """Row r is rotated right by r positions."""
    return [s[r + 4 * ((c - r) % 4)] for c in range(4) for r in range(4)]


def mix_columns(s):
    """Each column is multiplied by a fixed matrix (2 3 1 1 ...)."""
    out = []
    for c in range(4):
        a0, a1, a2, a3 = s[4 * c:4 * c + 4]
        out += [gmul(a0, 2) ^ gmul(a1, 3) ^ a2 ^ a3,
                a0 ^ gmul(a1, 2) ^ gmul(a2, 3) ^ a3,
                a0 ^ a1 ^ gmul(a2, 2) ^ gmul(a3, 3),
                gmul(a0, 3) ^ a1 ^ a2 ^ gmul(a3, 2)]
    return out


def inv_mix_columns(s):
    """Inverse matrix (14 11 13 9 ...) used for decryption."""
    out = []
    for c in range(4):
        a0, a1, a2, a3 = s[4 * c:4 * c + 4]
        out += [gmul(a0, 14) ^ gmul(a1, 11) ^ gmul(a2, 13) ^ gmul(a3, 9),
                gmul(a0, 9) ^ gmul(a1, 14) ^ gmul(a2, 11) ^ gmul(a3, 13),
                gmul(a0, 13) ^ gmul(a1, 9) ^ gmul(a2, 14) ^ gmul(a3, 11),
                gmul(a0, 11) ^ gmul(a1, 13) ^ gmul(a2, 9) ^ gmul(a3, 14)]
    return out


def aes_encrypt_block(block, key, show):
    rk = key_expansion(key)
    s = add_round_key(list(block), rk[0])           # Round 0
    if show:
        show_state("Round 0 - AddRoundKey", s)

    rnd = 1
    while rnd <= 10:                                # 10 rounds
        s = sub_bytes(s)
        if show:
            show_state("Round %d - SubBytes" % rnd, s)
        s = shift_rows(s)
        if show:
            show_state("Round %d - ShiftRows" % rnd, s)
        if rnd != 10:                               # last round has no MixColumns
            s = mix_columns(s)
            if show:
                show_state("Round %d - MixColumns" % rnd, s)
        s = add_round_key(s, rk[rnd])
        if show:
            show_state("Round %d - AddRoundKey" % rnd, s)
        else:
            print("  Round %2d: %s" % (rnd, bytes(s).hex().upper()))
        rnd += 1
    return bytes(s)


def aes_decrypt_block(block, key, show):
    rk = key_expansion(key)
    s = add_round_key(list(block), rk[10])
    rnd = 9
    while rnd >= 0:                                 # go backwards
        s = inv_shift_rows(s)
        s = inv_sub_bytes(s)
        s = add_round_key(s, rk[rnd])
        if show:
            show_state("Round %d (inverse) - after InvShiftRows, InvSubBytes, AddRoundKey" % rnd, s)
        else:
            print("  Round %2d: %s" % (rnd, bytes(s).hex().upper()))
        if rnd != 0:
            s = inv_mix_columns(s)                  # no InvMixColumns at the very end
        rnd -= 1
    return bytes(s)


def aes_menu():
    last_cipher = ""
    last_key = ""
    while True:
        print("\n------ AES MENU ------")
        print("1. Encrypt   (one text up to 16 chars, filled with Z = plaintext AND key)")
        print("2. Decrypt")
        print("3. Back")
        ch = input("Choice: ").strip()

        if ch == "1":
            text = get_text_z("Enter up to 16 characters (plaintext = key, rest filled with Z): ", 16)
            key = text.encode("utf-8")                  # same bytes used as plaintext AND key
            last_key = text
            show = input("Show every step? (y/n): ").lower() == "y"
            print("\nPlaintext = Key = %s" % text)
            cipher = aes_encrypt_block(key, key, show)  # 1 block, no padding needed
            last_cipher = cipher.hex().upper()
            print("\n>>> CIPHERTEXT (hex):", last_cipher)

        elif ch == "2":
            s = input("Ciphertext hex%s: " % (" (Enter = last one)" if last_cipher else "")).strip()
            s = s or last_cipher
            key = get_text_z("Key (the same text%s): " %
                             (", Enter = last one" if last_key else ""), 16, last_key).encode("utf-8")
            show = input("Show every step? (y/n): ").lower() == "y"
            try:
                cipher = bytes.fromhex(s)
                if len(cipher) != 16:
                    raise ValueError("ciphertext must be exactly 32 hex digits")
                plain = aes_decrypt_block(cipher, key, show)
                print("\n>>> PLAINTEXT (hex):", plain.hex().upper())
                print(">>> PLAINTEXT (text):", plain.decode("utf-8", errors="replace"))
            except ValueError as e:
                print("\n  Decryption failed:", e)

        elif ch == "3":
            break
        else:
            print("  Please choose 1, 2 or 3.")


# =====================================================================
#                           MAIN MENU (while loop)
# =====================================================================
while True:
    print("\n==============================")
    print("  1. DES")
    print("  2. AES")
    print("  3. Exit")
    print("==============================")
    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        des_menu()
    elif choice == "2":
        aes_menu()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("  Please choose 1, 2 or 3.")