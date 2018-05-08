#!python3
"""\
This module creates PEP-272 cipher object classes for building block ciphers
in python.

To use, inherit the PEP272Cipher and overwrite
``encrypt_block`` or ``decrypt_block(self, key, string, **kwargs)`` methods
and set the block_size attribute.


Example:

::

 class YourCipher(PEP272Cipher):
     block_size=8

     def encrypt_block(self, key, string, **kwargs):
         ...

     def decrypt_block(self, key_string, **kwargs):
         ...


"""

from .util import xor_strings, b_chr, b_ord
from .version import *


MODE_ECB = 1  #:
MODE_CBC = 2  #:
MODE_CFB = 3  #:
MODE_PGP = 4  #:
MODE_OFB = 5  #:
MODE_CTR = 6  #:


class PEP272Cipher:
    """
    A cipher object as defined in PEP-272_.

    Subclass and overwrite the encrypt_block and decrypt_block methods and
    the block_size attribute.

    .. _PEP-272: https://www.python.org/dev/peps/pep-0272/

    """
    block_size = NotImplemented
    IV = None

    def __init__(self, key, mode, **kwargs):
        if not key:
            raise ValueError("'key' cannot have a length of 0")
        self.key = key
        self.mode = mode
        self.IV = kwargs.pop('IV', None) or kwargs.pop('iv', None)
        self._status = self.IV

        self.segment_size = kwargs.pop('segment_size', 8)
        self._counter = kwargs.pop('counter', None)

        self.kwargs = kwargs

        self._check_arguments()
        self._keystream = self._create_keystream()


    def _check_arguments(self):
        """
        Checks if all required keyword arguments have been set.

        Tests for:
            - IV when using MODE_CBC, MODE_CFB, MODE_OFB
            - callable counter with MODE_CTR

        """
        if self.mode in (MODE_CBC, MODE_CFB, MODE_OFB, MODE_PGP):
            if self._status is None:
                raise TypeError("For CBC, CFB, PGP and OFB mode an IV is "
                                "required.")
            if len(self._status) != self.block_size and self.mode != MODE_PGP:
                raise ValueError("'IV' length must be block_size ({})".format(
                    self.block_size))
            elif self.mode == MODE_PGP:
                if not len(self._status) in (self.block_size, self.block_size+2):
                    raise ValueError(
                        ("'IV' length must be block_size ({})"
                         "or blocksize + 2".format(self.block_size)))

        if self.mode == MODE_CFB:
            if not self.segment_size:
                raise TypeError("missing required positional argument for CFB:"
                                " 'segment_size'")
            if not (8 <= self.segment_size <= self.block_size*8) or (
                    self.segment_size % 8):
                raise TypeError("segment_size must be between 8 and "
                                "block_size*8 and a multiple of 8")

        if self.mode == MODE_CTR:
            if self._counter is None:
                raise TypeError("missing required positional argument for CTR:"
                                " 'counter'")
            if not callable(self._counter):
                raise TypeError("counter must be a callable, it is not")


    def encrypt(self, string):
        """blabla docstring"""
        if self.mode in (MODE_OFB, MODE_CTR):
            return self._encrypt_with_keystream(string)

        out = []

        if self.mode == MODE_CFB:
            for block in _block(string, self.segment_size // 8):
                encrypted_iv = self.encrypt_block(self.key, self._status)
                ecd = xor_strings(encrypted_iv, block)

                iv_p1 = self._status[self.segment_size//8:]
                iv_p2 = ecd

                self._status = iv_p1 + iv_p2

                out.append(ecd)

        elif self.mode in (MODE_ECB, MODE_CBC):
            for block in _block(string, self.block_size):
                if self.mode == MODE_ECB:
                    ecd = self.encrypt_block(self.key, block, **self.kwargs)
                elif self.mode == MODE_CBC:
                    xored = xor_strings(self._status, block)
                    ecd = self._status = self.encrypt_block(self.key, xored,
                                                       **self.kwargs)

                out.append(ecd)

        else:
            raise ValueError("Unknown mode of operation")

        return b"".join(out)


    def decrypt(self, string):
        """blabla docstring"""
        if self.mode in (MODE_OFB, MODE_CTR):
            return self.encrypt(string)

        out = []

        if self.mode == MODE_CFB:
            for block in _block(string, self.segment_size // 8):
                encrypted_iv = self.encrypt_block(self.key, self._status)
                dec = xor_strings(encrypted_iv, block)

                iv_p1 = self._status[self.segment_size//8:]
                iv_p2 = block

                self._status = iv_p1 + iv_p2

                out.append(dec)

        elif self.mode in (MODE_ECB, MODE_CBC):
            for block in _block(string, self.block_size):
                if self.mode == MODE_ECB:
                    dec = self.decrypt_block(self.key, block, **self.kwargs)
                elif self.mode == MODE_CBC:
                    decrypted_but_not_xored = self.decrypt_block(self.key, block,
                                                                 **self.kwargs)
                    dec = xor_strings(self._status, decrypted_but_not_xored)
                    self._status = block

                out.append(dec)

        else:
            raise ValueError("Unknown mode of operation")

        return b"".join(out)

    def encrypt_block(self, key, block, **kwargs):
        """Dummy function for the encryption of a single block.
Overwrite with 'real' encryption function.

Raises NotImplementedError."""
        raise NotImplementedError

    def decrypt_block(self, key, block, **kwargs):
        """Dummy function for the decryption of a single block.
Overwrite with 'real' decryption function.

Raises NotImplementedError."""
        raise NotImplementedError

    def _encrypt_with_keystream(self, data):
        "Encrypts data with the set keystream."
        xor = [x ^ y for (x, y) in zip(map(b_ord, data),
                                              self._keystream)]
        return bytes(bytearray(xor))  # Faster


    def _create_keystream(self):
        "Creates a keystream (generator object) for OFB or CTR mode."
        if self.mode not in (MODE_OFB, MODE_CTR):
            # Coverage somehow does not work here
            return  # pragma: no cover

        while True:
            if self.mode == MODE_OFB:
                _next = self._status
            elif self.mode == MODE_CTR:
                _next = self._counter()
                if len(_next) != self.block_size:
                    raise TypeError("Counter length must be block_size")

            self._status = self.encrypt_block(self.key, _next, **self.kwargs)

            for k in self._status:
                yield b_ord(k)


def _block(bytestring, block_size):
    """Splits bytestring in block_size-sized blocks.

Raises an error if len(string) % blocksize != 0.
"""
    if block_size == 1:
        return map(b_chr, bytearray(bytestring))

    rest_size = len(bytestring) % block_size

    if rest_size:
        raise ValueError("Input 'bytestring' must be a multiple of block_size / "
                         "segment_size (CFB mode) in length")

    block_count = len(bytestring) // block_size

    return (
        bytestring[i * block_size:((i + 1) * block_size)]
        for i in range(block_count))
