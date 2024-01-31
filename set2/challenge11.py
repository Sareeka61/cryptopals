from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random
import string

def generate_random_aes_key():
    return get_random_bytes(16)

def generate_random_bytes(length):
    return get_random_bytes(random.randint(5, 10))

def pkcs7_pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encryption_oracle(plaintext):
    key = generate_random_aes_key()
    prepend_bytes = generate_random_bytes(random.randint(5, 10))
    append_bytes = generate_random_bytes(random.randint(5, 10))
   
    plaintext = prepend_bytes + plaintext + append_bytes

    # Randomly choose between ECB and CBC mode
    mode = random.randint(0, 1)
    if mode == 0:
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = pkcs7_pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, "ECB"
    else:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = pkcs7_pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, "CBC"

def detect_block_cipher_mode(ciphertext):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if len(blocks) != len(set(blocks)):
        return "ECB"
    else:
        return "CBC"

if __name__ == "__main__":
    plaintext = b"Hello, this is a test message."
    ciphertext, mode_used = encryption_oracle(plaintext)
    detected_mode = detect_block_cipher_mode(ciphertext)
    
    print("Mode used by the oracle:", mode_used)
    print("Detected mode by detection function:", detected_mode)
