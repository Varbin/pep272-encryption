"""
Utility library for compatability with Python 2 and 3.

This includes versions of ``chr`` and ``ord``-methods to work with bytes
with Python 3 and strings with Python 2.
"""

import sys

try:
    from ._fast_xor import _fast_xor
except ImportError:
    raise
    _fast_xor = None

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

    if _fast_xor is None:
        one, two = bytearray(one), bytearray(two)
        result = bytearray(x ^ y for x, y in zip(one, two))
    else:
        result = _fast_xor(one, len(one), two, len(two))

    return bytes(result)
