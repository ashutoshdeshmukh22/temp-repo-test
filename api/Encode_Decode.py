from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode

key = "cngUKQjtKStwGG7RLWix6YkXWfnyQ4lz".encode('utf-8')
iv = base64.b64decode("AAAAAAAAAAAAAAAAAAAAAA==")

class DecodeEncodeString():

    def __init__(self, request_token):
        self.message = request_token
    
    def get_token(self):
        decStr = self.decryptAPIString(self.message.encode())
        
        # Replace the number at the end
        split_string = decStr.decode('UTF-8').split("|")
        new_string = f"{split_string[1]}|{split_string[0]}" 

        # Encrypt String again
        encStr = self.encryptAPIString(new_string)
        return encStr
    
    def encryptAPIString(self,plaintext):
        raw = plaintext.encode('utf-8')
        encryptor = Cipher(algorithms.AES(key),modes.GCM(iv, None, 16), default_backend()).encryptor()
        ciphertext = encryptor.update(raw) + encryptor.finalize()
        return self.base64UrlEncode(ciphertext+encryptor.tag)

    def decryptAPIString(self, ciphertext):
        enc = self.base64UrlDecode(ciphertext)[:-16]
        decryptor = Cipher(algorithms.AES(key),modes.GCM(iv), default_backend()).decryptor()
        return decryptor.update(enc)

    def base64UrlEncode(self, data):
        return urlsafe_b64encode(data).rstrip(b'=')

    def base64UrlDecode(self, base64Url):
        padding = b'=' * (4 - (len(base64Url) % 4))
        return urlsafe_b64decode(base64Url + padding)

if __name__ == "__main__":
    obj = DecodeEncodeString(request_token="qfJ4CzlZKRXkOgggKWPT-98CZrKzc1w-HZalzn6IwMce3akeEosqJm6Zz45rIGUGtDWpWSo7_vA=")
    print(obj.get_token())
