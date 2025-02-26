from cryptography.fernet import Fernet
from ..config import Config

key = Config.SECRET_KEY
cipher_suite = Fernet(key)

def encrypt(data):
    return cipher_suite.encrypt(data.encode())

def decrypt(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()