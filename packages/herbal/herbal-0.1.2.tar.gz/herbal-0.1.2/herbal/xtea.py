from ctypes import c_uint32 as uint32_t

from herbal.block_cipher import KEY_SCHEDULE
from herbal.types_ import Block64, Block128


def xtea_code_block(v: Block64, k: Block128, n: int, /) -> Block64:
    """
    Extended TEA block encoding algorithm.

    https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.

    :param Block64 v: 64-bit block as two unsigned 32-bit integers.
    :param Key128 k: 128-bit key as four unsigned 32-bit integers.
    :param int n: Number of coding cycles. If `n` is +ve, encodes the
        `v` block. If `n` is -ve, decodes the `v` block. Does nothing
        if `n` is 0.
    :return Block64: Output 64-bit block.
    """
    y, z = v

    if n > 0:
        limit = KEY_SCHEDULE.value * n
        sum_ = uint32_t(0)
        while sum_.value != limit:
            y.value += (
                z.value << 4 ^ z.value >> 5
            ) + z.value ^ sum_.value + k[sum_.value & 3].value
            sum_.value += KEY_SCHEDULE.value
            z.value += (
                y.value << 4 ^ y.value >> 5
            ) + y.value ^ sum_.value + k[sum_.value >> 11 & 3].value
    elif n < 0:
        sum_ = uint32_t(KEY_SCHEDULE.value * -n)
        while sum_:
            z.value -= (
                y.value << 4 ^ y.value >> 5
            ) + y.value ^ sum_.value + k[sum_.value >> 11 & 3].value
            sum_.value -= KEY_SCHEDULE.value
            y.value -= (
                z.value << 4 ^ z.value >> 5
            ) + z.value ^ sum_.value + k[sum_.value & 3].value

    return y, z
