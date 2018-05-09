.. _install:

Installation
------------

Like the most python libraries, ``pep272-encryption`` can be installed with
pip_ from PyPi_.

To install just open a console and run:

::

   $ pip install pep272_encryption


That's it!

.. _pip: https://pypi.org/project/pip/
.. _PyPi: https://pypi.org/project/pep272-encryption/

Development version
*******************

To get the newest features, it is possible to directly install the latest
version from GitHub_:

::

    $ pip install git+https://github.com/Varbin/pep272-encryption


.. _GitHub: https://github.com/Varbin/pep272-encryption

Supported platforms
*******************

``pep272-encryption`` is pure Python with optional Cython speedups,
so any architecture is supported. 
It supports Python 2.7 and 3.4+. It might work with Python 3.3, but is not
tested with it.

For tests CPython is required because the (old) PyCrypto package is required.
PyCryptodome will **not work**!
