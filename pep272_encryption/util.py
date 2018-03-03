"""
Util library for compatability with Python 2 and 3.

Functions:
    b_ord(n): like ord(n) over the iteration product of a bytestring
    b_chr(n): bytestring from number between 0-255
    xor_strings(s, t): xor two bytestrings
"""

import sys

PY_3 = sys.version_info.major >= 3

if PY_3:

    def b_chr(ordinal):
        "Return a byte string of one character with 0 <= ordinal <= 255."
        return bytes([ordinal])
else:

    def b_chr(ordinal):
        "Return a byte string of one character with 0 <= ordinal <= 255."
        return chr(ordinal)


def b_ord(byte):
    "Return the Unicode code point for a byte or iteration product \
of a byte string alike object (e.g. bytearray)."
    return byte if isinstance(byte, int) else ord(byte)


def xor_strings(one, two):
    """xor to bytestrings together.
    Keyword arguments:
    one -- string one
    two -- string two
    """
    return b"".join(b_chr(b_ord(x) ^ b_ord(y)) for x, y in zip(one, two))
