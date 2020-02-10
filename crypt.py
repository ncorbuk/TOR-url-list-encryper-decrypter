from Crypto.Random import new as Random
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
from hashlib import sha256
import argparse


def args_parser():
    parser = argparse.ArgumentParser(description='filename -o e(encrypt)/d(decrypt) filename key')
    parser.add_argument('-o', '--crypter', type=str, required=True, help='encrypt/decrypt/dec+enc file // -o e, d, de')
    parser.add_argument('-f', '--filename', type=str, required=False, default='d:/tmp/tmp/abc.txt', help='filename')
    parser.add_argument('-k', '--key', type=str, required=True, help='key')
    args = parser.parse_args()
    return args


class AESCipher:
    def __init__(self, filename, key):
        self.block_size = 16
        self.filename = args_parser().filename
        self.key = sha256(key.encode('utf8')).digest()[:32]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr((self.block_size - len(s) % self.block_size))
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])]

    def readfile(self):
        with open(self.filename, 'r') as f:
            data = f.read()
            text = self.pad(data)
            return text

    def writefile(self, x):
        with open(self.filename, 'w') as f:
            f.write(x)

    def encrypt(self):
        plain_text = self.readfile()
        iv = Random().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_OFB, iv)
        a = base64.b64encode(iv + cipher.encrypt(bytes(plain_text, 'utf8'))).decode()
        self.writefile(a)

    def decrypt(self):
        encrpyt_text = self.readfile()
        cipher_text = base64.b64decode(encrpyt_text)
        iv = cipher_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_OFB, iv)
        b = self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()
        print(b)
        self.writefile(b)


def encrypt():
    E = AESCipher(filename=args_parser().filename, key=args_parser().key)
    E.encrypt()

def decrypt():
    E = AESCipher(filename=args_parser().filename, key=args_parser().key)
    E.decrypt()


def main():
    crypterr = args_parser().crypter
    try:
        if crypterr == 'e':
            encrypt()
    except Exception as e:
        print('> Encryption failed.')
    try:
        if crypterr == 'd':
            decrypt()
    except Exception as e:
        print('> Decryption failed')
    try:
        if crypterr == 'de':
            decrypt()
            encrypt()
    except Exception as e:
        print('> Dec+Enc failed.')



if __name__ == '__main__':
    main()
