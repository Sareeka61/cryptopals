from challenge3 import xor_decrypt

english_letter_frequency = {
    'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425,
    'e': 0.1270, 'f': 0.0223, 'g': 0.0202, 'h': 0.0609,
    'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
    'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193,
    'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
    'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
    'y': 0.0197, 'z': 0.0007, ' ': 0.1300
}

def score_text(text):
    score = 0
    for char in text.lower():
        if char in english_letter_frequency:
            score += english_letter_frequency[char]
    return score

def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)

hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

ciphertext = hex_to_bytes(hex_string)

best_score = 0
best_plaintext = ''
best_key = None

for key in range(256):
    decrypted_text = xor_decrypt(ciphertext, key)
    score = score_text(decrypted_text)
    if score > best_score:
        best_score = score
        best_plaintext = decrypted_text
        best_key = key

print("Best Key:", chr(best_key))
print("Decrypted Text:", best_plaintext)
