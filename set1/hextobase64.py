import binascii
import base64

# Input hexadecimal string
hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

# Converting hex to bytes
bytes_data = binascii.unhexlify(hex_string)

# Encoding bytes to Base64
base64_string = base64.b64encode(bytes_data).decode('utf-8')

# Printing the result
print("Hex:", hex_string)
print("Raw:", bytes_data)
print("Base64:", base64_string)
