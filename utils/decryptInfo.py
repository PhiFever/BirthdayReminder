#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle

import yaml

from utils.cipherIO import CipherIO


def get_env(env_name: str) -> str:
    """Get the value of an environment variable."""
    try:
        return os.environ[env_name]
    except KeyError:
        raise ValueError(f"Environment variable {env_name} not found")


def decrypt_info(cipher, peopleCipherPath) -> list:
    people = pickle.loads(cipher.read_cipher_yaml(peopleCipherPath))
    return people


if __name__ == '__main__':
    key = get_env("KEY").encode('utf-8')  # 对朋友的信息进行对称加密的密钥

    curPath = os.path.dirname(os.path.realpath(__file__))
    peoplePath = os.path.join(curPath, "../config/peopleInfo.yaml")
    peopleCipherPath = os.path.join(curPath, "../config/peopleCipherInfo.yaml")
    cipher = CipherIO(key)

    if os.path.exists(peopleCipherPath):
        people = decrypt_info(cipher, peopleCipherPath)

        # 写入到yaml文件
        with open(peoplePath, "w", encoding="utf-8") as f:
            yaml.dump(people, f, allow_unicode=True)

        print("Decrypt peopleInfo.yaml successfully!")
