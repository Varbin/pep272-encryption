.. image:: https://img.shields.io/travis/Varbin/pep272-encryption.svg
    :target: https://travis-ci.org/Varbin/pep272-encryption

.. image:: https://img.shields.io/codecov/c/github/Varbin/pep272-encryption/master.svg
    :target: https://codecov.io/gh/Varbin/pep272-encryption

`Documentation <https://sbiewald.de/docs/pep272-encryption/>`_

To prevent reinventing the wheel while creating a 
`PEP-272 <https://www.python.org/dev/peps/pep-0272/>`_ interface for a new 
block cipher encryption, this library aims to create an extensible framework 
for new libraries.

Currently following modes of operation are supported:

- ECB
- CBC
- CFB
- OFB 
- CTR

The `PGP mode of operation <https://tools.ietf.org/html/rfc4880#section-13.9>`_ 
is not supported. It may be added in the future.

Example
-------

In this example ``encrypt_aes(key, block)`` will encrypt one block of AES while
``decrypt_aes(key, block)`` will decrypt one.

>>> from pep272_encryption import PEP272Cipher, MODE_ECB
>>> class AESCipher:
...    """
...    PEP-272 cipher class for AES
...    """
...    block_size = 16
...
...    def encrypt_block(self, key, block, **kwargs):
...        return encrypt_aes(key, block)
...        
...    def decrypt_block(self, key, block, **kwargs):
...        return decrypt_aes(key, block)
...     
>>> cipher = AESCipher(b'\00'*16, MODE_ECB)
>>> cipher.encrypt(b'\00'*16)
b'f\xe9K\xd4\xef\x8a,;\x88L\xfaY\xca4+.'

License
-------

This project is licensed under `CC0 <https://creativecommons.org/publicdomain/zero/1.0/>`_ 
(public domain).
