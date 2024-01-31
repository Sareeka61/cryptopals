def pad_pkcs7(message, block_size):
    pad_length = block_size - len(message) % block_size
    padding = bytes([pad_length]) * pad_length
    return message + padding

message = b"YELLOW SUBMARINE"
padded_message = pad_pkcs7(message, 20)
print(padded_message)
