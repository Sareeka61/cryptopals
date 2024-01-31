import base64
from itertools import combinations
from collections import Counter
import string

def hamming_distance(s1, s2):
    return sum(bin(c1 ^ c2).count('1') for c1, c2 in zip(s1, s2))

def normalized_edit_distance(text, keysize):
    chunks = [text[i:i+keysize] for i in range(0, len(text), keysize)][:4]  # Take first 4 blocks
    total_distance = sum(hamming_distance(chunk1, chunk2) for chunk1, chunk2 in combinations(chunks, 2))
    return total_distance / (keysize * 6)  # Normalize by dividing by keysize * number of comparisons

def find_keysize(ciphertext):
    distances = {}
    for keysize in range(2, 41):
        distances[keysize] = normalized_edit_distance(ciphertext, keysize)
    return min(distances, key=distances.get)

def transpose_blocks(ciphertext, keysize):
    transposed_blocks = [b'' for _ in range(keysize)]
    for i in range(len(ciphertext)):
        transposed_blocks[i % keysize] += bytes([ciphertext[i]])
    return transposed_blocks

def single_char_xor(ciphertext):
    candidates = []
    for char in range(256):
        decrypted = bytes(c ^ char for c in ciphertext)
        score = sum(chr(c).lower() in string.ascii_lowercase + ' ' for c in decrypted)
        candidates.append((score, decrypted, char))
    return max(candidates)

def decrypt_repeating_xor(ciphertext):
    keysize = find_keysize(ciphertext)
    transposed_blocks = transpose_blocks(ciphertext, keysize)
    key = ''
    for block in transposed_blocks:
        _, _, char = single_char_xor(block)
        key += chr(char)
    plaintext = bytes(ciphertext[i] ^ ord(key[i % len(key)]) for i in range(len(ciphertext)))
    return plaintext.decode()

with open('./challenge6.txt', 'r') as file:
    ciphertext = base64.b64decode(file.read())

plaintext = decrypt_repeating_xor(ciphertext)
print(plaintext)
