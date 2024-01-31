from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import quote, unquote

AES_KEY = b'\xfd\x04\x18\xe5\xe7\x1b\xfb!\x8b\xcdm\x08k4\x02p'

def encrypt_userdata(input_string):
    # Prepend and append the input string
    input_string = "comment1=cooking%20MCs;userdata=" + quote(input_string) + ";comment2=%20like%20a%20pound%20of%20bacon"
    # Pad the input string to the 16-byte AES block length
    padded_input = pad(input_string.encode(), AES.block_size)
    # Initialize AES cipher in CBC mode
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV=b'\x00' * AES.block_size)
    # Encrypt the padded input
    ciphertext = cipher.encrypt(padded_input)
    return ciphertext

def check_for_admin(ciphertext):
    # Initialize AES cipher in CBC mode
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV=b'\x00' * AES.block_size)
    # Decrypt the ciphertext
    decrypted_data = cipher.decrypt(ciphertext)
    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)
    # Check for admin string in the decrypted data
    if b';admin=true;' in unpadded_data:
        return True
    else:
        return False

def bit_flipping_attack():
    # Craft a plaintext block to manipulate the ciphertext
    # We want to flip bits to change the first block to "admin=true;"
    crafted_block = b'\x00' * AES.block_size
    # Define the target string we want to insert
    target_string = b';admin=true;xxxx'
    # Define the position in the block to start flipping bits
    start_position = 16
    # Perform the bit flipping attack
    for i in range(len(target_string)):
        # Calculate the position in the ciphertext where we need to flip the bits
        pos = start_position + i
        # Calculate the value we need to XOR with the current ciphertext byte to get the desired byte
        xor_value = target_string[i] ^ crafted_block[pos - start_position]
        # Flip the bits by XORing with the calculated value
        crafted_block = crafted_block[:pos] + bytes([xor_value]) + crafted_block[pos + 1:]
    return crafted_block


if __name__ == "__main__":
    # Encrypt the crafted input
    ciphertext = encrypt_userdata("A" * 16)
    # Perform the bit flipping attack
    crafted_block = bit_flipping_attack()
    # Modify the ciphertext by XORing it with the crafted block
    modified_ciphertext = bytes([a ^ b for a, b in zip(ciphertext[:AES.block_size], crafted_block)]) + ciphertext[AES.block_size:]
    # Check if the modified ciphertext contains the admin string
    if check_for_admin(modified_ciphertext):
        print("Admin access granted!")
    else:
        print("Admin access denied!")
