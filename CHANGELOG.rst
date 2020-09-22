Changelog
=========

0.4
---

New
***

- Type hints
- Build manylinux wheels

Changed
*******

- Extension module is in pure C, removing the requirement of Cython

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
