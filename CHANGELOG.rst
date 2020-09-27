Changelog
=========

0.4
---

New
***

- Type hints
- Build manylinux wheels, universal wheel is limited to Python 2 and PyPy
- In addition to callables, the *counter* argument for CTR mode now accepts counters from PyCryptodome now

Changed
*******

- Extension module is in pure C, instead of being written in Cython
- *__init__* signature is slightly different:

  - *IV* can be given as a positional argument
  - *counter* and *segment_size* are keyword only,
    but are named

0.3 - 2019-06-14
----------------

Added
*****

- ``PEP272Cipher`` is a new style class on Python 2.
- Documentation
- Optional extensions module for more speed. CBC and CFB are now two times faster!

Changed
*******

- ``PEP272Cipher.IV`` does not change in mode using a CBC

0.1 - 2019-03-03
----------------

- Initial release.
