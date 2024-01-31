def fixedXOR(buffer1, buffer2):
    bytes1 = bytes.fromhex(buffer1)
    bytes2 = bytes.fromhex(buffer2)

    resultbytes = bytes(x^y for x, y in zip(bytes1, bytes2))

    resulthex = resultbytes.hex()

    return resulthex

buffer1 = "1c0111001f010100061a024b53535009181c"

buffer2 = "686974207468652062756c6c277320657965"

result = fixedXOR(buffer1, buffer2)

print("buffer1 =", buffer1)
print("buffer2 =", buffer2)
print("XOR result =", result)