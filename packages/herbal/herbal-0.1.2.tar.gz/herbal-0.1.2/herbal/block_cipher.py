"""herbal.block_cipher: convert data to and from uint32 blocks."""

import os
import struct
from ctypes import c_uint32 as uint32_t
from hashlib import scrypt
from typing import Iterable

from herbal.types_ import Block64, Block128

# 2^32 / 𝜙 (golden ratio)
KEY_SCHEDULE = uint32_t(int(2**32 / ((1 + 5**0.5) / 2)))


def derive_key(password: bytes, *, salt: bytes) -> Block128:
    """
    Securely derive a 128-bit encryption key from a given password.

    Uses the scrypt key derivation function.

    :param bytes password: Password bytes object.
    :param bytes salt: Random data to prevent rainbow table cracking.
    :return Block128: Key represented as four unsigned 32-bit integers.
    """
    size = 16  # 128 bits.
    key = scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=size)
    a, b, c, d = (uint32_t(i) for i in struct.unpack(">4I", key))
    return a, b, c, d


def to_blocks(data: bytes, add_padding: bool = False) -> Iterable[Block64]:
    """
    Convert bytes into a sequence of uint32 blocks.

    :param bytes data: Bytes data to be converted.
    :param add_padding bool: Add padding to data, defaults to False.
    :yield Iterable[Block64]: Sequence of two unsigned 32-bit integers.
    """
    size = 8  # 64 bits.
    if add_padding:
        # Add random padding to prevent errors with smaller block sizes.
        pad = size - len(data) % size
        data += os.urandom(pad - 1) + pad.to_bytes(1, "big")
    uint32_array = (
        struct.unpack(">2I", data[i : i + size])
        for i in range(0, len(data), size)
    )
    blocks = ((uint32_t(y), uint32_t(z)) for (y, z) in (uint32_array))
    yield from blocks


def from_blocks(
    blocks: Iterable[Block64], remove_padding: bool = False
) -> bytes:
    """
    Convert a sequence of uint32 blocks into bytes.

    :param Iterable[Block64] blocks: Sequence of two unsigned 32-bit
        integers.
    :param remove_padding bool: Remove padding from data, defaults
        to False.
    :return bytes: Bytestring representation.
    """
    data = b"".join(struct.pack(">2I", y.value, z.value) for y, z in blocks)
    if remove_padding:
        # Remove padding from data.
        return data[: -data[-1]]
    return data
