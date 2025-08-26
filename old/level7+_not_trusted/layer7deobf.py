# xor_transform.py
"""
Однострочный декодер (и одновременно кодер) для строк,
зашифрованных функцией `u1KQ2EguJKQ7` из obf‑скрипта.

Использование
-------------
>>> from xor_transform import decrypt, encrypt
>>> raw = b"Hello, world!"
>>> enc = encrypt(raw)          # шифруем
>>> dec = decrypt(enc)          # обратно
>>> dec == raw                  # True
"""

from typing import ByteString, Union

# 40‑байтовый ключ, который автор пытался скрыть
KEY: bytes = bytes.fromhex(
    "3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00"
    "031e18071d0f1a0a"
)


def xor_transform(data: ByteString, key: bytes = KEY) -> bytes:
    """
    Универсальная функция XOR‑преобразования.
    Для исходного алгоритма ENCRYPT == DECRYPT.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes‑like object")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


# удобные алиасы --------------------------------------------------------------
encrypt = xor_transform
decrypt = xor_transform

__all__ = ["KEY", "xor_transform", "encrypt", "decrypt"]