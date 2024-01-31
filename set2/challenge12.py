from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

unknown_string_base64 = (
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28g"
    "bXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
)
unknown_string = base64.b64decode(unknown_string_base64)

global_key = get_random_bytes(16)

def encryption_oracle(plaintext):
    global unknown_string
    global global_key

    plaintext += unknown_string

    block_size = 16
    padding_length = block_size - (len(plaintext) % block_size)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    cipher = AES.new(global_key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def detect_ecb(ciphertext):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if len(blocks) != len(set(blocks)):
        return True
    else:
        return False

def determine_block_size():
    initial_length = len(encryption_oracle(b""))
    for i in range(1, 256):
        plaintext = b"A" * i
        new_length = len(encryption_oracle(plaintext))
        if new_length > initial_length:
            return new_length - initial_length

def decrypt_unknown_string():
    block_size = determine_block_size()
    is_ecb = detect_ecb(encryption_oracle(b"A" * 64))

    if not is_ecb:
        return "Not using ECB mode"

    decrypted_text = b""
    num_blocks = len(encryption_oracle(b"")) // block_size

    for block_num in range(num_blocks):
        for byte_num in range(block_size):
            target = encryption_oracle(b"A" * (block_size - 1 - byte_num))[block_num*block_size:(block_num+1)*block_size]
            for i in range(256):
                trial = b"A" * (block_size - 1 - byte_num) + decrypted_text + bytes([i])
                output = encryption_oracle(trial)[block_num*block_size:(block_num+1)*block_size]
                if output == target:
                    decrypted_text += bytes([i])
                    break
    return decrypted_text

if __name__ == "__main__":
    decrypted_text = decrypt_unknown_string()
    print(decrypted_text.decode())
