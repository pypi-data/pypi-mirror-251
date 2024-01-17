"""Python package for the Tiny Encryption Algorithm (TEA)."""

from herbal.tea import decrypt as tea_decode
from herbal.tea import encrypt as tea_encode

__all__ = ["tea_encode", "tea_decode"]
__version__ = "0.1.2"
