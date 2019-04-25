
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):

    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(plaintext))

    def decrypt(self, encrypted):
        encrypted = base64.b64decode(encrypted)
        iv = encrypted[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(encrypted[AES.block_size:]))


    @staticmethod
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

