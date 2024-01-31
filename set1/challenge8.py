def detect_ecb(ciphertexts):
    for ciphertext in ciphertexts:
        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        unique_blocks = set(blocks)
        if len(unique_blocks) != len(blocks):
            return ciphertext
    return None

if __name__ == "__main__":
    with open('./challenge8.txt', 'r') as file:
        ciphertexts = [bytes.fromhex(line.strip()) for line in file]

    result = detect_ecb(ciphertexts)
    if result:
        print("ECB mode detected in ciphertext:")
        print(result.hex())
    else:
        print("ECB mode not detected.")
