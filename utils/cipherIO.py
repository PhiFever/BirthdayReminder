#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.cryption import encrypt, decrypt


class CipherIO:
    def __init__(self, key: bytes):
        self.plain_text = None
        self.key = key

    # 将密文写入文件
    def create_cipher_yaml(self, plaintext: bytes, cipherPath: str):
        with open(cipherPath, 'wb') as cipher_file:
            cipher_text = encrypt(self.key, plaintext)
            cipher_file.write(cipher_text)

    # 从密文读取文件
    def read_cipher_yaml(self, cipherPath: str):
        with open(cipherPath, 'rb') as cipher_file:
            cipher_text = cipher_file.read()
            # print(cipher_text)
            self.plain_text = decrypt(self.key, cipher_text)
            return self.plain_text
