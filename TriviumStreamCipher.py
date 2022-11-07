# API


def _hex_to_bytes(s):
    return [_allbytes[s[i:i+2].upper()] for i in range(0, len(s), 2)]


def _bytes_to_hex(s):
    return ''.join(format(X, '02X') for X in s)


def bits_to_hex(b):
    return "".join(["%02X" % sum([b[i + j] << j for j in range(8)]) for i in range(0, len(b), 8)])


def hex_to_bits(s):
    return [(b >> i) & 1 for b in _hex_to_bytes(s) for i in range(8)]


_allbytes = dict([("%02X" % i, i) for i in range(256)])


def add_head(t, s):
    s.insert(0, t)
    s.pop()


def rotate(s1, s2, s3):
    k1 = s1[65] ^ s1[92]
    k2 = s2[68] ^ s2[83]
    k3 = s3[65] ^ s3[110]

    z = k1 ^ k2 ^ k3

    a1 = s1[90] & s1[91]
    a2 = s2[81] & s2[82]
    a3 = s3[108] & s3[109]

    t1 = k1 ^ a1 ^ s2[77]
    t2 = k2 ^ a2 ^ s3[86]
    t3 = k3 ^ a3 ^ s1[68]

    add_head(t3, s1)
    add_head(t1, s2)
    add_head(t2, s3)

    return z


def init_state(s1, s2, s3):
    for i in range(4 * 288):
        rotate(s1, s2, s3)


def key_stream(s1, s2, s3):
    for i in range(2**64):
        yield rotate(s1, s2, s3)


# __main__
plaintext = "Hanoi University of Science and Technology"
key_string = "0F62B5085BAE0154A7FA"
iv_string = "288FF65DC42B92F960C7"
print("Key: " + key_string)
print("IV:  " + iv_string)

# parse KEY and IV from string to 80bits
KEY = hex_to_bits(key_string)[::-1]
IV = hex_to_bits(iv_string)[::-1]
# initializal internal state
s1_s93 = KEY
s94_s177 = IV
s178_s288 = []
for i in range(13):
    s1_s93.append(0)
s94_s177 = s94_s177 + [0, 0, 0, 0]
for i in range(108):
    s178_s288.append(0)
s178_s288 = s178_s288 + [1, 1, 1]
init_state(s1_s93, s94_s177, s178_s288)

# key_stream
next_key_bit = key_stream(s1_s93, s94_s177, s178_s288)
keystream = []
for j in range(8*len(plaintext)):
    keystream.append(next(next_key_bit))

# encrypto
print("====================Encrypto====================")
print("Plaintext:  " + "'" + plaintext + "'")
plaintext_dec = []
for i in range(len(plaintext)):
    plaintext_dec.append((ord(plaintext[i])))
print(plaintext_dec)
print("Key stream: " + bits_to_hex(keystream))
key_stream_dec = _hex_to_bytes(bits_to_hex(keystream))
print(key_stream_dec)
ciphertext = ''
ciphertext_dec = []
for i in range(len(plaintext)):
    cipher = plaintext_dec[i] ^ key_stream_dec[i]
    ciphertext_dec.append(cipher)
    ciphertext += chr(cipher)
print("Ciphertext: " + "'" + ciphertext + "'")
print("Ciphertext Hexa: " + (_bytes_to_hex(ciphertext_dec)).upper())

# decrypto
print("====================Decrypto====================")
plain_text = ''
for i in range(len(ciphertext)):
    plain = ciphertext_dec[i] ^ key_stream_dec[i]
    plain_text += chr(plain)
print("Plaintext: " + "'" + plain_text + "'")
