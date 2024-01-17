"""herbal.tea: original 1994 TEA block cipher implementation."""

import os
from base64 import b85decode, b85encode
from ctypes import c_uint32 as uint32_t
from typing import overload

from herbal.block_cipher import (
    KEY_SCHEDULE,
    derive_key,
    from_blocks,
    to_blocks,
)
from herbal.types_ import Block64, Block128, String

__all__ = ["encrypt", "decrypt"]


def tea_encode_block(v: Block64, k: Block128, /) -> Block64:
    """
    TEA block encoding algorithm.

    https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.

    :param Block64 v: Unencoded 64-bit block as two unsigned 32-bit
        integers.
    :param Key128 k: 128-bit key as four unsigned 32-bit integers.
    :return Block64: Encoded 64-bit block.
    """
    y, z = v
    sum_ = uint32_t(0)
    for _ in range(32):
        sum_.value += KEY_SCHEDULE.value
        y.value += (
            ((z.value << 4) + k[0].value)
            ^ (z.value + sum_.value)
            ^ ((z.value >> 5) + k[1].value)
        )
        z.value += (
            ((y.value << 4) + k[2].value)
            ^ (y.value + sum_.value)
            ^ ((y.value >> 5) + k[3].value)
        )
    return y, z


def tea_decode_block(v: Block64, k: Block128, /) -> Block64:
    """
    TEA block decoding algorithm.

    https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.

    :param Block64 v: Encoded 64-bit block as two unsigned 32-bit
        integers.
    :param Key128 k: 128-bit key as four unsigned 32-bit integers.
    :return Block64: Decoded 64-bit block.
    """
    y, z = v
    sum_ = uint32_t(KEY_SCHEDULE.value << 5)
    for _ in range(32):
        z.value -= (
            ((y.value << 4) + k[2].value)
            ^ (y.value + sum_.value)
            ^ ((y.value >> 5) + k[3].value)
        )
        y.value -= (
            ((z.value << 4) + k[0].value)
            ^ (z.value + sum_.value)
            ^ ((z.value >> 5) + k[1].value)
        )
        sum_.value -= KEY_SCHEDULE.value

    return y, z


@overload
def encrypt(plaintext: str, password: String) -> str:
    ...


@overload
def encrypt(plaintext: bytes, password: String) -> bytes:
    ...


def encrypt(plaintext: String, password: String) -> String:
    """
    Encrypt the provided plaintext using the TEA block cipher.

    >>> herbal.tea_encode("hello, world! :3", password="secret")

    :param String plaintext: String to be encrypted.
    :param String password: Password to derive the encryption key from.
    :return String: Encrypted ciphertext.
    """
    data_type = type(plaintext)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    if isinstance(password, str):
        password = password.encode()

    salt = os.urandom(16)
    key = derive_key(password, salt=salt)
    blocks = to_blocks(plaintext, add_padding=True)
    encoded_blocks = (tea_encode_block(i, key) for i in blocks)
    ciphertext = from_blocks(encoded_blocks)
    output = b85encode(salt) + b":" + b85encode(ciphertext)

    if data_type is str:
        return output.decode()
    return output


@overload
def decrypt(ciphertext: str, password: String) -> str:
    ...


@overload
def decrypt(ciphertext: bytes, password: String) -> bytes:
    ...


def decrypt(ciphertext: String, password: String) -> String:
    """
    Decrypt the provided ciphertext using the TEA block cipher.

    >>> herbal.tea_decode(
    ...     "____)$x>_HL%IQu6Gn|A:E4h?9Cdc>N"
    ...     "DjFwP`;Ya1Qd6{O1;8JV%Nq}4(qY++",
    ...     password="secret"
    ... )

    :param String plaintext: String to be decrypted.
    :param String password: Password to derive the encryption key from.
    :return String: Decrypted plaintext.
    """
    data_type = type(ciphertext)
    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()
    if isinstance(password, str):
        password = password.encode()

    salt, ciphertext = (b85decode(i) for i in ciphertext.split(b":"))

    if len(ciphertext) % 8:
        raise NotImplementedError("String bytes must be a multiple of 8.")

    key = derive_key(password, salt=salt)
    encoded_blocks = to_blocks(ciphertext)
    decoded_blocks = (tea_decode_block(i, key) for i in encoded_blocks)
    plaintext = from_blocks(decoded_blocks, remove_padding=True)
    if data_type is str:
        return plaintext.decode()
    return plaintext
