import nacl.secret
import nacl.utils
from nacl.utils import EncryptedMessage


def encrypt(key: bytes, plain_text: bytes) -> EncryptedMessage:
    # This is your safe, you can use it to encrypt or decrypt messages
    box = nacl.secret.SecretBox(key)

    # Encrypt our message, it will be exactly 40 bytes longer than the
    # original message as it stores authentication information and the
    # nonce alongside it.
    cipher_text = box.encrypt(plain_text)
    assert len(cipher_text) == len(plain_text) + box.NONCE_SIZE + box.MACBYTES

    return cipher_text


def decrypt(key: bytes, cipher_text: EncryptedMessage) -> str:
    # This is your safe, you can use it to encrypt or decrypt messages
    box = nacl.secret.SecretBox(key)

    # Decrypt our message, an exception will be raised if the encryption was
    #   tampered with or there was otherwise an error.
    plain_text = box.decrypt(cipher_text)
    return plain_text.decode('utf-8')


if __name__ == "__main__":
    # This is our message to send, it must be a bytestring as SecretBox
    # We will treat it as just a binary blob of data.
    # Here are examples of how to encrypt and decrypt
    message = '{"Name": "张三", "Birthdate": "1997-12-06", "Calendar": "lunar", "Email": ""}'
    plaintext = bytes(message, 'utf-8')
    key = b"12345678901234567890123456789012"

    ciphertext = encrypt(key, plaintext)
    print(ciphertext)

    loadtext = decrypt(key, ciphertext)
    print(loadtext)
