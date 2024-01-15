"""
passlib.tests -- tests for passlib.utils.md4

.. warning::

    This module & it's functions have been deprecated, and superceded
    by the functions in passlib.crypto.  This file is being maintained
    until the deprecated functions are removed, and is only present prevent
    historical regressions up to that point.  New and more thorough testing
    is being done by the replacement tests in ``test_utils_crypto_builtin_md4``.
"""
#=============================================================================
# imports
#=============================================================================
# core
import warnings
# site
# pkg
# module
from passlib.tests.test_crypto_builtin_md4 import _Common_MD4_Test
# local
__all__ = [
    "Legacy_MD4_Test",
]
#=============================================================================
# test pure-python MD4 implementation
#=============================================================================
class Legacy_MD4_Test(_Common_MD4_Test):
    descriptionPrefix = "passlib.utils.md4.md4()"

    def setUp(self):
        super(Legacy_MD4_Test, self).setUp()
        warnings.filterwarnings("ignore", ".*passlib.utils.md4.*deprecated", DeprecationWarning)

    def get_md4_const(self):
        from passlib.utils.md4 import md4
        return md4

#=============================================================================
# eof
#=============================================================================
