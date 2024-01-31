from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def aes_ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def aes_cbc_encrypt(plaintext, key, iv):
    ciphertext = b""
    previous_block = iv

    for i in range(0, len(plaintext), AES.block_size):
        block = plaintext[i:i + AES.block_size]

        xor_result = xor_bytes(block, previous_block)

        encrypted_block = aes_ecb_encrypt(xor_result, key)

        previous_block = encrypted_block

        ciphertext += encrypted_block

    return ciphertext

if __name__ == "__main__":
    plaintext = b"Attack at dawn!"
    key = get_random_bytes(AES.block_size)
    iv = bytes([0] * AES.block_size)

    ciphertext = aes_cbc_encrypt(plaintext, key, iv)
    print("Ciphertext:", ciphertext.hex())
