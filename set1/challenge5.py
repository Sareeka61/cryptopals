def repeating_key_xor(text, key):
    encrypted_bytes = b''
    key_length = len(key)
    for i in range(len(text)):
        encrypted_byte = text[i] ^ key[i % key_length]
        encrypted_bytes += bytes([encrypted_byte])
    return encrypted_bytes.hex()

plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

plaintext_bytes = plaintext.encode()
key_bytes = key.encode()

encrypted_text = repeating_key_xor(plaintext_bytes, key_bytes)
print(encrypted_text)
