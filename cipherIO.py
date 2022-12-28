#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cryption import encrypt, decrypt


class CipherIO:
    def __init__(self, key: bytes):
        self.key = key

    # 将密文写入文件
    def createCipherYaml(self, plaintext: bytes, cipherPath: str):
        cipherFile = open(cipherPath, 'wb')
        cipherText = encrypt(self.key, plaintext)
        cipherFile.write(cipherText)
        cipherFile.close()

    # 从密文读取文件
    def readCipherYaml(self, cipherPath: str):
        cipherFile = open(cipherPath, 'rb')
        cipherText = cipherFile.read()
        self.plaintext = decrypt(self.key, cipherText)
        return self.plaintext
