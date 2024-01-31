import base64
from Crypto.Cipher import AES

# Read the encrypted content from the file
with open('./challenge7.txt', 'rb') as file:
    encrypted_content = base64.b64decode(file.read())

# Define the key
key = b'YELLOW SUBMARINE'

# Create an AES cipher object in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt the content
decrypted_content = cipher.decrypt(encrypted_content)

# Print the decrypted content
print(decrypted_content.decode())
