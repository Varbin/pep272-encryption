cimport cython

@cython.embedsignature(True)
def fast_xor(unsigned char *a, int la, unsigned char *b, int lb):
    """
    Fast bitwise xor between to buffers.

    The correct lengths have to be passed to work and security,
    output length is min(la, lb), returns bytearray.
    """
    cdef int i
    cdef bytearray c = bytearray(min(la, lb))

    for i in range(min(la, lb)):
        c[i] = a[i] ^ b[i]

    return c
