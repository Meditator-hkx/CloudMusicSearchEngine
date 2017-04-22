# coding: utf-8

import os
import base64
from Crypto.Cipher import AES

TEXT = {'username': '', 'password': '', 'rememberLogin': 'true'}
MODULUS = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
NONCE = '0CoJUm6Qyw8W8jud'
PUBKEY = '010001'


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