.. _howto:

How-To
======

In this section practical solutions to problems are shown.

New mode of operation
---------------------

For this example a fictional blockcipher mode of operation is added, 
lets call it "mask codebook mode": 
A fixed mask is xored to each plaintext block, everything else works like ECB.

1. Set Constant
***************

Which mode of operation is used is passed at initialization of the cipher
object.

Following name / number assigments are common:

+------------------+--------+
| Constant         | Number |
+==================+========+
| ``MODE_ECB``     | 1      |
+------------------+--------+
| ``MODE_CBC``     | 2      |
+------------------+--------+
| ``MODE_CFB``     | 3      |
+------------------+--------+
| ``MODE_PGP``     | 4      |
+------------------+--------+
| ``MODE_OFB``     | 5      |
+------------------+--------+
| ``MODE_CTR``     | 6      |
+------------------+--------+
| ``MODE_OPENPGP`` | 7      |
+------------------+--------+
| ``MODE_CCM`` or  |        |
| ``MODE_XTS``     | 8      |
+------------------+--------+
| ``MODE_EAX``     | 9      |
+------------------+--------+
| ``MODE_SIV``     | 10     |
+------------------+--------+
| ``MODE_GCM``     | 11     |
+------------------+--------+
| ``MODE_OCB``     | 12     |
+------------------+--------+

To avoid incompatabilities, the correspondenting number should not be on of
above.

::

    MODE_MCB = 500 

seems a solid choice.

2. Skeleton
***********

A subclass of ``PEP272Cipher`` is made, with a new init parameter `mask`:

::

    from pep272_encryption import PEP272Cipher

    class MCBCapableCipher(PEP272Cipher):
        def __init__(self, key, mode, **kwargs):
            self.mask = kwargs.pop(mask, b'\x00'*self.block_size)
            PEP272Cipher.__init__(self, key, mode, **kwargs)

        def encrypt(self, string):
            if self.mode == MODE_MCB:
                ...
            else:
                PEP272Cipher.encrypt(string)

        def decrypt(self, string):
            if self.mode == MODE_MCB:
                ...
            else:
                PEP272Cipher.decrypt(string)


3. Implementation
*****************

Obviously the new mode bust be implemented. To use the blocks of a message
and raise errors the helper function ``_block(bytestring, blocksize)`` exists.

::

        def encrypt(self, string):
            if self.mode == MODE_MCB:
                out = []
                for block in _block(string, self.block_size):
                    masked = xor_string(self.mask, block)
                    encrypted = self.encrypt_block(masked)
                    out.append(encrypted)
                return b"".join(masked)
       
            else:
                PEP272Cipher.encrypt(string)

        def decrypt(self, string):
            if self.mode == MODE_MCB:
                out = []
                for block in _block(string, self.block_size):
                    maksed = self.decrypt_block(block)
                    plain = xor_string(self.mask, masked)
                    out.append(plain)
                return b"".join(masked)
            else:
                PEP272Cipher.decrypt(string)

That's it!
