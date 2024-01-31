def validate_and_strip_padding(plaintext):
    padding_length = plaintext[-1]
    if padding_length > len(plaintext) or padding_length == 0:
        raise ValueError("Invalid padding")

    expected_padding = bytes([padding_length]) * padding_length
    if plaintext[-padding_length:] != expected_padding:
        raise ValueError("Invalid padding")

    stripped_plaintext = plaintext[:-padding_length]
    return stripped_plaintext

try:
    plaintext1 = "ICE ICE BABY\x04\x04\x04\x04".encode()
    print(validate_and_strip_padding(plaintext1).decode())  # Output: "ICE ICE BABY"

    plaintext2 = "ICE ICE BABY\x05\x05\x05\x05".encode()
    print(validate_and_strip_padding(plaintext2).decode())  # This line should raise a ValueError

    plaintext3 = "ICE ICE BABY\x01\x02\x03\x04".encode()
    print(validate_and_strip_padding(plaintext3).decode())  # This line should raise a ValueError

except ValueError as e:
    print("Error:", str(e))
