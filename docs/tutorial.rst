Tutorial
========

*PEP-272 compliant TEA cipher*

.. note:: 
   Before starting, first things first: This library is for creating 
   *block cipher implementations* only! 
   It does not contain or implement any ciphers by itself.

0. The TEA block cipher
-----------------------

In this tutorial the TEA block cipher will be used as the underlying block 
cipher and give it a PEP-272 interface.

TEA uses 128-bit (16 bytes) keys and 64-bit (8 bytes) blocks.


In Python, an unoptimized version of TEA can be written like following:

::

    import struct

    def encrypt_tea(value, key, endian="!", rounds=64):
        v0, v1 = struct.unpack(endian + "2L", value)
        k = struct.unpack(endian + "4L", key)

        # mask is an uint32 helper
        delta, mask, sum = 0x9e3779b9, 0xffffffff, 0

        for i in range(rounds//2):
            sum = (sum + delta) & mask
            v0 = v0 + ( ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]) ) & mask
            v1 = v1 + ( ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]) ) & mask

        return struct.pack(endian + "2L", v0, v1)

    def decrypt_tea(value, key, endian="!", rounds=64):
        v0, v1 = struct.unpack(endian + "2L", value)
        k = struct.unpack(endian + "4L", key)

        # mask is an uint32 helper
        delta, mask = 0x9e3779b9, 0xffffffff
        sum = (delta * rounds // 2) & mask

        for i in range(rounds//2):
            v1 = v1 - ( ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]) ) & mask
            v0 = v0 - ( ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]) ) & mask
            sum = (sum - delta) & mask

        return struct.pack(endian + "2L", v0, v1)

(It runs slow because integers can get quite big before the mask is applied.)

1. Project skeleton
-------------------

To begin, write import the most important pep272-encryption module:

::

   from pep272_encryption import PEP272Cipher, MODE_ECB, MODE_CBC, \
                                               MODE_CFB, MODE_OFB, \
                                               MODE_CTR

2. Setting parameters
---------------------

Next define some module level constants, as defined per PEP-272:

::

   block_size = 8  # 64-bit blocks
   key_size = 16   # 128-bit keys


3. Subclassing
--------------

Subclass the PEP272Cipher class, setting the block size parameter and
override `encrypt_block` and `decrypt_block` methods:

::

   class TEACipher(PEP272Cipher):
       block_size = block_size

       def encrypt_block(self, key, block, **kwargs):
           return encrypt_tea(block, key, 
                              kwargs.get('endian', '!'), 
                              kwargs.get('rounds', 64))

       def decrypt_block(self, key, block, **kwargs):
           return decrypt_tea(block, key, 
                              kwargs.get('endian', '!'), 
                              kwargs.get('rounds', 64))


4. Alternative constructor (`new`-method)
-----------------------------------------

An alternative constructor is usefull for interoperbility:

::

   def new(*args, **kwargs):
       return TEACipher(*args, **kwargs)

5. Full example code
--------------------

Below is the full example code with all snippets combined: A PEP-272 compliant
implementation of the TEA block cipher in pure python, that is interchangeble
with other ciphers.

.. literalinclude:: _static/tea.py
   :linenos:


Download full example: tea.py_

.. _tea.py: ./_static/tea.py

6. Usage
--------

Now the newly created library can be used easily.

Example: Encrypt some data in OFB mode.

::

   >>> import tea
   >>> cipher = tea.new(b'16-bytes key 123', mode=tea.MODE_OFB, IV=b'\00'*9)
   >>> cipher.encrypt(b'123456'*6)
   b"k\xaf F\xfb*\xeb\x00'kP\x9c\xc9M\xb99\x1cy\xda\x99\xb1\xf0H\x14\x9c\xae@\xddxe`\x01\x85\xc9p\x85"

