import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import quote, unquote


def parse_query(query):
    pairs = query.split('&')
    parsed = {}
    for pair in pairs:
        key, value = pair.split('=')
        parsed[key] = value
    return parsed


def encode_profile(email):
    sanitized_email = email.replace('&', '').replace('=', '')
    profile = {
        'email': sanitized_email,
        'uid': 10,
        'role': 'user'
    }
    encoded = '&'.join([f"{k}={v}" for k, v in profile.items()])
    return encoded


def encrypt_profile(profile, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(profile.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext


def decrypt_and_parse(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    decoded_profile = parse_query(unquote(unpadded_data.decode()))
    return decoded_profile


def generate_admin_profile():
    email = 'foo@bar.com'
    crafted_email = 'a' * 10 + 'admin' + '\x0b' * 11  # Padding to fill the block
    return encode_profile(crafted_email)


if __name__ == "__main__":
    key = os.urandom(16)

    email = "foo@bar.com"
    profile = encode_profile(email)

    ciphertext = encrypt_profile(profile, key)

    admin_profile = generate_admin_profile()

    decrypted_admin_profile = decrypt_and_parse(encrypt_profile(admin_profile, key), key)

    print("Attacker's Role=admin Profile:", decrypted_admin_profile)
