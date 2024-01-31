from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import os

AES_KEY = os.urandom(16)

def generate_random_prefix():
    return os.urandom(10)

def encryption_oracle(input_bytes, target_bytes):
    plaintext = generate_random_prefix() + input_bytes + target_bytes
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

def detect_block_size():
    initial_length = len(encryption_oracle(b'', b''))
    for i in range(1, 65):
        input_bytes = b'A' * i
        new_length = len(encryption_oracle(input_bytes, b''))
        if new_length != initial_length:
            return new_length - initial_length

def detect_ecb_mode(block_size):
    input_bytes = b'A' * block_size * 3
    ciphertext = encryption_oracle(input_bytes, b'')
    if ciphertext[:block_size] == ciphertext[block_size:2*block_size]:
        return True
    return False

def decrypt_target_bytes(block_size):
    target_length = len(encryption_oracle(b'', b''))
    decrypted_bytes = b''
    for byte_index in range(target_length):
        padding_size = block_size - (byte_index % block_size) - 1
        crafted_input = b'A' * padding_size
        intermediate_dict = {}
        for test_byte in range(256):
            test_input = crafted_input + decrypted_bytes + bytes([test_byte])
            intermediate_dict[encryption_oracle(test_input, b'')[:target_length]] = bytes([test_byte])
        crafted_input = crafted_input + decrypted_bytes
        target_block = encryption_oracle(crafted_input, b'')[:target_length]
        decrypted_bytes += intermediate_dict[target_block]
    return decrypted_bytes

if __name__ == "__main__":
    block_size = detect_block_size()
    print("Detected block size:", block_size)
    if detect_ecb_mode(block_size):
        print("ECB mode detected.")
        decrypted_target_bytes = decrypt_target_bytes(block_size)
        print("Decrypted target bytes:", decrypted_target_bytes)
    else:
        print("ECB mode not detected. Aborting.")
