.. _api:

Library reference
=================

.. automodule:: pep272_encryption

The PEP272Cipher class
--------------------------

Subclass and overwrite the PEP272Cipher.encrypt_block and 
PEP272Cipher.decrypt_block methods and the block_size attribute.

.. autoclass:: pep272_encryption.PEP272Cipher
   :members:

.. _api-modes:

Block cipher mode of operation
------------------------------

.. note::
    For mote details about different modes of operation,
    see Discussions/:ref:`discussion-modes`.

.. _PEP-272: https://www.python.org/dev/peps/pep-0272/

Block ciphers can be used in different modes of operation.
The mode of operation can be set by passing one of the constants
to the cipher object. Different modes of operation may require to pass extra
arguments to the constructor.

Below is an example from the mostly PEP-272_ compliant  PyCryptodome_.

.. _PyCrypto: https://www.dlitz.net/software/pycrypto/
.. _PyCryptodome: https://www.pycryptodome.org/ 

::

   >>> from Crypto.Cipher import AES
   >>> iv = b'random 16 bytes!'
   >>> key = b'0123456789abcdef'
   >>> cipher = AES.new(key, mode=AES.MODE_CBC, IV=iv)
   >>> cipher.encrypt(b'\00'*16)
   b'j\xa2\xb5\x80\xf7\xbd\xb4I\xda\xea\x9aN\x9d\xb5\x9a\x17'

This library supports following modes of operation:

 - Electronic code book (ECB)
 - Cipher Block Chaining (CBC)
 - Cipher Feedback (CFB)
 - Output Feedback (OFB)
 - Counter (CTR)

Not supported is, but may be implemented in the future:

 - PGP variant of CFB (PGP)

Planned modes are (extending to PEP-272_):

 - Propagating Cipher Block Chaining (PCBC), used in older Kerberos versions
 - Infinite Garble Extension (IGE), used by Telegram.
 - OpenPGP mode, compatible to PyCrypto_ or PyCryptodome_.

`Authenticated encryption (AE) or authenticated encryption with associated data 
(AEAD)`_ will probably not be supported, as they would require additional 
methods to finalize the encryption and sometimes have special requirements.

.. _Authenticated encryption (AE) or authenticated encryption with associated data (AEAD): https://en.wikipedia.org/wiki/Authenticated_encryption

Electronic Code Book Mode (ECB)
+++++++++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_ECB

.. warning::
   The ECB mode is not `semantically secure`_.

.. _semantically secure: https://en.wikipedia.org/wiki/Semantic_security

The ECB mode of operation is the simplest one - each plaintext block is 
independently encrypted.

:param test: bla

Cipher Block Chaining Mode (CBC)
++++++++++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_CBC

To solve the problems of the ECB mode, a plaintext block is xored_ to the
previous ciphertext block. For the very "first" ciphertext an 
**initialization vector (IV)** is used.

Plain- / ciphertexts must be multiple of blocksize in length.

.. _xored: https://en.wikipedia.org/wiki/Exclusive_or

Cipher Feedback Mode (CFB)
++++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_CFB

The CFB mode of operation makes a stream cipher out of the block cipher. The 
block size of the cipher is reduced to ``segment_size``.

Plain- and ciphertext must be a multiple of ``segment_size`` in length.

Output Feedback (OFB)
+++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_OFB

OFB uses a CBC encryption of a stream of null bytes to create a keystream.


Counter mode of operation
+++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_CTR

CTR encrypts a counter to create a keystream.

Utility functions
-----------------

.. automodule:: pep272_encryption.util
   :members:

Version information and metadata
--------------------------------

.. automodule:: pep272_encryption.version

.. autodata:: pep272_encryption.version.__version__
.. autodata:: pep272_encryption.version.__author__
.. autodata:: pep272_encryption.version.__email__
.. autodata:: pep272_encryption.version.__license__
.. autodata:: pep272_encryption.version.__url__
