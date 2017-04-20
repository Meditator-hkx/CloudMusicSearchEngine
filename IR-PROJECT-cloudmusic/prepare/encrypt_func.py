# coding: utf-8

import os
import base64
from Crypto.Cipher import AES 


def create_secret_key(size):
    """
    Create a secret key whose length is 16.

    :param size:
    :return:
    """
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


def aes_encrypt(text, sec_key):
    """
    AES encrypt method.

    :param text:
    :param sec_key:
    :return:
    """
    pad = 16 - len(text) % 16
    text += pad * chr(pad)
    encryptor = AES.new(sec_key, 2, '0102030405060708')
    cipher_text = encryptor.encrypt(text)
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text


def rsa_encrypt(text, pub_key, modulus):
    """
    RSA encrypt method.

    :param text:
    :param pub_key:
    :param modulus:
    :return:
    """
    text = text[::-1]
    rs = int(text.encode('hex'), 16) ** int(pub_key, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)