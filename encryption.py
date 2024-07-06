import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def generate_key(password, salt):
    """
    Generates a cryptographic key based on the given password and salt using PBKDF2HMAC.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes = 256 bits
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(data, password):
    """
    Encrypts the given data using AES encryption with the provided password.
    """
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return base64.urlsafe_b64encode(salt + iv + encrypted_data).decode('utf-8')

def decrypt(encrypted_data, password):
    """
    Decrypts the given encrypted data using AES decryption with the provided password.
    """
    encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
    salt, iv, encrypted_data = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()
