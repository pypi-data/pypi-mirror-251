"""herbal.types_: define type aliases used in the package."""

from ctypes import c_uint32 as uint32_t
from typing import Union

Block64 = tuple[uint32_t, uint32_t]
Block128 = tuple[uint32_t, uint32_t, uint32_t, uint32_t]
String = Union[str, bytes]
