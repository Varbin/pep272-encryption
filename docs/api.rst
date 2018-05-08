Library reference
=================

.. automodule:: pep272_encryption

The PEP272Cipher class
--------------------------

.. autoclass:: pep272_encryption.PEP272Cipher
   :members:


Block cipher mode of operation
------------------------------

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
independently encrypted. The resulting problem is that the same plaintext
leads to the same ciphertext.

Plain- / ciphertexts must be multiple of blocksize in length.

The formulae for the ECB mode are:

.. math::
 
   C_{i}=E_{K}(P_{i})

   P_{i}=D_{K}(C_{i})


.. figure::  https://upload.wikimedia.org/wikipedia/commons/d/d6/ECB_encryption.svg
   :align:   center

   ECB encryption

.. figure::  https://upload.wikimedia.org/wikipedia/commons/e/e6/ECB_decryption.svg
   :align:   center

   ECB decryption

Attacks against ECB mode
************************

Because all plaintext blocks are encrypted independently, an encryption
of the same block results in the same ciphertext block each time.

This means by having multiple ciphertexts in can be concluded whether the 
correspondent plaintexts are the same or not.

The multiple repetition of plaintext blocks may result in visible repetitions
in the ciphertext, e.g. in images.

.. figure::  https://upload.wikimedia.org/wikipedia/commons/5/56/Tux.jpg
   :align:   center

   Plain Tux image

.. figure::  https://upload.wikimedia.org/wikipedia/commons/f/f0/Tux_ecb.jpg
   :align:   center

   Encrypted Tux image in ECB mode


Cipher Block Chaining Mode (CBC)
++++++++++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_CBC

.. note::
   The CBC mode of operation requires the extra parameter ``IV``, which must
   be unpredictable (e.g. random) for optimal security and must be used only
   once.

.. warning::
   The IV must never be used twice, it would totally break the security.

To solve the problems of the ECB mode, a plaintext block is xored_ to the
previous ciphertext block. For the very "first" ciphertext an 
**initialization vector (IV)** is used. The IV can be considered public
information.

Plain- / ciphertexts must be multiple of blocksize in length.

Having an incorrect block or IV will result in an incorrect decryption of
the direct adjectant block, but the remaining blocks will remain intact.

The formulae for en- and decryption are:

.. math::
 
   C_{i}=E_{K}(P_{i} \oplus C_{i-1})

   P_{i}=D_{K}(C_{i}) \oplus C_{i-1})

   C_0 = \mbox{IV}


.. _xored: https://en.wikipedia.org/wiki/Exclusive_or

.. figure::  https://upload.wikimedia.org/wikipedia/commons/8/80/CBC_encryption.svg
   :align:   center

   CBC encryption

.. figure::  https://upload.wikimedia.org/wikipedia/commons/2/2a/CBC_decryption.svg
   :align:   center

   CBC decryption

Attacks against CBC mode
************************

A one-bit change  to the ciphertext causes complete corruption of the 
corresponding block of plaintext, and the inversion of the corresponding bit
in the next block while leaving the rest iof the blocks intact. This can lead
to `padding oracle attacks`_ such as POODLE_ (it is the consequence solely
of the choice of CBC mode but other design choices, too).

`Watermarking attacks`_ are possible with predictable IVs.

.. _padding oracle attacks: https://en.wikipedia.org/wiki/Padding_oracle_attack
.. _POODLE: https://en.wikipedia.org/wiki/POODLE
.. _Watermarking attacks: https://en.wikipedia.org/wiki/Watermarking_attack

Cipher Feedback Mode (CFB)
++++++++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_CFB

.. note::
   The CFB mode of operation requires the extra parameter ``IV``, which must
   be unpredictable (e.g. random) for optimal security and must be used only
   once.

   The extra parameter ``segment_size`` in bits
   (between 8 and 8 :math:`\cdot` block size in bytes) must passed, too.

.. warning::
   The IV must never be used twice, it would totally break the security.

The CFB mode of operation makes a stream cipher out of the block cipher. The 
block size of the cipher is reduced to ``segment_size``.

Plain- and ciphertext must be a multiple of ``segment_size`` in length.

The formulae describing CFB mode are:

.. math::

   C_{i}=E_{K}(C_{i-1})\oplus P_{i}

   P_{i}=E_{K}(C_{i-1})\oplus C_{i}

   C_{0}=\mbox{IV}


.. figure::  https://upload.wikimedia.org/wikipedia/commons/9/9d/CFB_encryption.svg
   :align:   center

   CFB encryption

.. figure::  https://upload.wikimedia.org/wikipedia/commons/5/57/CFB_decryption.svg
   :align:   center

   CFB decryption


Output Feedback (OFB)
+++++++++++++++++++++

.. autodata:: pep272_encryption.MODE_OFB

.. note::
   The OFB mode of operation requires the extra parameter ``IV``, which must
   be unpredictable (e.g. random) for optimal security and must be used only
   once.

.. warning::
   The IV must never be used twice, it would totally break the security.

OFB mode creates a stream cipher by xoring_ the plain text with a keystream
generated by encrypting a stream of null bytes in CBC mode. Encryption
and decryption are the same, data of arbitrary length can be processed.

The formulae describing OFB mode of operation are:

.. math::

   C_{i} = P_{i} \oplus O_{i}

   P_{i} = C_{i} \oplus O_{i}


   O_{i} = E_{K} (0_{i-1} \oplus 0 \ldots )

   O_{0}=\mbox{IV}


.. _xoring: https://en.wikipedia.org/wiki/Exclusive_or

.. figure::  https://upload.wikimedia.org/wikipedia/commons/b/b0/OFB_encryption.svg
   :align:   center

   OFB encryption

.. figure::  https://upload.wikimedia.org/wikipedia/commons/f/f5/OFB_decryption.svg
   :align:   center

   OFB decryption


Counter mode of operation
+++++++++++++++++++++++++


.. autodata:: pep272_encryption.MODE_CTR

.. note::
   The CTR mode of operation requires the extra parameter ``counter``. It must
   be a callable, returning a byte string (byte-alike on Python 3, string or
   byte-alike on Python 2).

.. warning::
   The return value of ``counter()`` must never be the same value twice for the
   same key.

CTR mode creates a stream cipher by xoring_ the plain text with a keystream
generated by encrypting counter. Encryption
and decryption are the same, data of arbitrary length can be processed.

CTR can be described with those formulae:

.. math::

   C_{i} = P_{i} \oplus O_{i}

   P_{i} = C_{i} \oplus O_{i}

where :math:`O_{i}` are the return values of the counter.


.. figure::  https://upload.wikimedia.org/wikipedia/commons/4/4d/CTR_encryption_2.svg
   :align:   center

   CTR encryption

.. figure::  https://upload.wikimedia.org/wikipedia/commons/3/3c/CTR_decryption_2.svg
   :align:   center

   CTR decryption

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
