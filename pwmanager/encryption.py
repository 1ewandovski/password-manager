# import packages for encryption
import base64
import string
from random import randint, choice
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random as CryptoRandom
from hashlib import sha256
from uuid import uuid4

class Encryption():

    def __init__(self, key):
        self.key = key  # Key in bytes
        self.salted_key = None  # Placeholder for optional salted key

    def digest_key(self):
        """
            Use SHA-256 over our key to get a proper-sized AES key
        """

        # Add optional salt to key
        key = self.key
        if self.salted_key:
            key = self.salted_key

        return SHA256.new(key).digest()

    def get_aes(self, IV):
        """
            AES instance
        """

        return AES.new(self.digest_key(), AES.MODE_CBC, IV)

    def gen_salt(self, set_=True):
        """
            Generate a random salt
        """

        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.punctuation + string.digits
        salt = "".join(choice(allchar)
                       for x in range(randint(min_char, max_char))).encode()

        # Set the salt in the same instance if required
        if set_:
            self.set_salt(salt)

        return salt

    def set_salt(self, salt=None):
        """
            Add a salt to the secret key for this specific encryption or decryption
        """

        if salt:
            self.salted_key = salt + self.key
        else:
            self.salted_key = None

    def encrypt(self, secret):
        """
            Encrypt a secret
        """

        # generate IV
        IV = CryptoRandom.new().read(AES.block_size)

        # Retrieve AES instance
        aes = self.get_aes(IV)

        # calculate needed padding
        padding = AES.block_size - len(secret) % AES.block_size

        # Python 2.x: secret += chr(padding) * padding
        secret += bytes([padding]) * padding

        # store the IV at the beginning and encrypt
        data = IV + aes.encrypt(secret)

        # Reset salted key
        self.set_salt()

        # Return base 64 encoded bytes
        return base64.b64encode(data)

    def decrypt(self, enc_secret):
        """
            Decrypt a secret
        """

        # Decode base 64
        enc_secret = base64.b64decode(enc_secret)

        # extract the IV from the beginning
        IV = enc_secret[:AES.block_size]

        # Retrieve AES instance
        aes = self.get_aes(IV)

        # Decrypt
        data = aes.decrypt(enc_secret[AES.block_size:])

        # pick the padding value from the end; Python 2.x: ord(data[-1])
        padding = data[-1]

        # Python 2.x: chr(padding) * padding
        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")

        # Reset salted key
        self.set_salt()

        # Remove the padding and return the bytes
        return data[:-padding]
      
# if __name__ == '__main__':
# 	main_password = 'password'
# 	email ='meredith-wu@sjtu.edu.cn'
# 	sub_pwd = '123sub_password'
# 	salt = str(uuid4())
# 	hash_pwd = sha256((email+salt+main_password).encode()).hexdigest()
# 	enc = Encryption(hash_pwd.encode())
# 	salt=enc.gen_salt()
# 	salt_save = salt.decode('utf-8')
# 	pwd_encrypt=enc.encrypt(sub_pwd.encode()).decode('utf-8')
# 	dec = Encryption(hash_pwd.encode())
# 	dec.set_salt(salt_save.encode())
# 	dec_pwd=dec.decrypt(pwd_encrypt.encode()).decode('utf-8')
# 	print(dec_pwd)