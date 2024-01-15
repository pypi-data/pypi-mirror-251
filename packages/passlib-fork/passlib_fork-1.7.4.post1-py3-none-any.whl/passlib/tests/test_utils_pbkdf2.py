"""
passlib.tests -- tests for passlib.utils.pbkdf2

.. warning::

    This module & it's functions have been deprecated, and superceded
    by the functions in passlib.crypto.  This file is being maintained
    until the deprecated functions are removed, and is only present prevent
    historical regressions up to that point.  New and more thorough testing
    is being done by the replacement tests in ``test_utils_crypto.py``.
"""
#=============================================================================
# imports
#=============================================================================
from __future__ import with_statement
# core
import hashlib
import warnings
# site
# pkg
# module
from passlib.utils.compat import u, JYTHON
from passlib.tests.utils import TestCase, hb

#=============================================================================
# test assorted crypto helpers
#=============================================================================
class UtilsTest(TestCase):
    """test various utils functions"""
    descriptionPrefix = "passlib.utils.pbkdf2"

    ndn_formats = ["hashlib", "iana"]
    ndn_values = [
        # (iana name, hashlib name, ... other unnormalized names)
        ("md5", "md5",          "SCRAM-MD5-PLUS", "MD-5"),
        ("sha1", "sha-1",       "SCRAM-SHA-1", "SHA1"),
        ("sha256", "sha-256",   "SHA_256", "sha2-256"),
        ("ripemd160", "ripemd-160", "SCRAM-RIPEMD-160", "RIPEmd160",
            # NOTE: there was an older "RIPEMD" & "RIPEMD-128", but python treates "RIPEMD"
            #       as alias for "RIPEMD-160"
            "ripemd", "SCRAM-RIPEMD"),
        ("test128", "test-128", "TEST128"),
        ("test2", "test2", "TEST-2"),
        ("test3_128", "test3-128", "TEST-3-128"),
    ]

    def setUp(self):
        super(UtilsTest, self).setUp()
        warnings.filterwarnings("ignore", ".*passlib.utils.pbkdf2.*deprecated", DeprecationWarning)

    def test_norm_hash_name(self):
        """norm_hash_name()"""
        from itertools import chain
        from passlib.utils.pbkdf2 import norm_hash_name
        from passlib.crypto.digest import _known_hash_names

        # test formats
        for format in self.ndn_formats:
            norm_hash_name("md4", format)
        self.assertRaises(ValueError, norm_hash_name, "md4", None)
        self.assertRaises(ValueError, norm_hash_name, "md4", "fake")

        # test types
        self.assertEqual(norm_hash_name(u("MD4")), "md4")
        self.assertEqual(norm_hash_name(b"MD4"), "md4")
        self.assertRaises(TypeError, norm_hash_name, None)

        # test selected results
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", '.*unknown hash')
            for row in chain(_known_hash_names, self.ndn_values):
                for idx, format in enumerate(self.ndn_formats):
                    correct = row[idx]
                    for value in row:
                        result = norm_hash_name(value, format)
                        self.assertEqual(result, correct,
                                         "name=%r, format=%r:" % (value,
                                                                  format))

#=============================================================================
# test PBKDF1 support
#=============================================================================
class Pbkdf1_Test(TestCase):
    """test kdf helpers"""
    descriptionPrefix = "passlib.utils.pbkdf2.pbkdf1()"

    pbkdf1_tests = [
        # (password, salt, rounds, keylen, hash, result)

        #
        # from http://www.di-mgt.com.au/cryptoKDFs.html
        #
        (b'password', hb('78578E5A5D63CB06'), 1000, 16, 'sha1', hb('dc19847e05c64d2faf10ebfb4a3d2a20')),

        #
        # custom
        #
        (b'password', b'salt', 1000, 0, 'md5',    b''),
        (b'password', b'salt', 1000, 1, 'md5',    hb('84')),
        (b'password', b'salt', 1000, 8, 'md5',    hb('8475c6a8531a5d27')),
        (b'password', b'salt', 1000, 16, 'md5', hb('8475c6a8531a5d27e386cd496457812c')),
        (b'password', b'salt', 1000, None, 'md5', hb('8475c6a8531a5d27e386cd496457812c')),
        (b'password', b'salt', 1000, None, 'sha1', hb('4a8fd48e426ed081b535be5769892fa396293efb')),
    ]
    if not JYTHON:
        pbkdf1_tests.append(
            (b'password', b'salt', 1000, None, 'md4', hb('f7f2e91100a8f96190f2dd177cb26453'))
        )

    def setUp(self):
        super(Pbkdf1_Test, self).setUp()
        warnings.filterwarnings("ignore", ".*passlib.utils.pbkdf2.*deprecated", DeprecationWarning)

    def test_known(self):
        """test reference vectors"""
        from passlib.utils.pbkdf2 import pbkdf1
        for secret, salt, rounds, keylen, digest, correct in self.pbkdf1_tests:
            result = pbkdf1(secret, salt, rounds, keylen, digest)
            self.assertEqual(result, correct)

    def test_border(self):
        """test border cases"""
        from passlib.utils.pbkdf2 import pbkdf1
        def helper(secret=b'secret', salt=b'salt', rounds=1, keylen=1, hash='md5'):
            return pbkdf1(secret, salt, rounds, keylen, hash)
        helper()

        # salt/secret wrong type
        self.assertRaises(TypeError, helper, secret=1)
        self.assertRaises(TypeError, helper, salt=1)

        # non-existent hashes
        self.assertRaises(ValueError, helper, hash='missing')

        # rounds < 1 and wrong type
        self.assertRaises(ValueError, helper, rounds=0)
        self.assertRaises(TypeError, helper, rounds='1')

        # keylen < 0, keylen > block_size, and wrong type
        self.assertRaises(ValueError, helper, keylen=-1)
        self.assertRaises(ValueError, helper, keylen=17, hash='md5')
        self.assertRaises(TypeError, helper, keylen='1')

#=============================================================================
# test PBKDF2 support
#=============================================================================
class Pbkdf2_Test(TestCase):
    """test pbkdf2() support"""
    descriptionPrefix = "passlib.utils.pbkdf2.pbkdf2()"

    pbkdf2_test_vectors = [
        # (result, secret, salt, rounds, keylen, prf="sha1")

        #
        # from rfc 3962
        #

            # test case 1 / 128 bit
            (
                hb("cdedb5281bb2f801565a1122b2563515"),
                b"password", b"ATHENA.MIT.EDUraeburn", 1, 16
            ),

            # test case 2 / 128 bit
            (
                hb("01dbee7f4a9e243e988b62c73cda935d"),
                b"password", b"ATHENA.MIT.EDUraeburn", 2, 16
            ),

            # test case 2 / 256 bit
            (
                hb("01dbee7f4a9e243e988b62c73cda935da05378b93244ec8f48a99e61ad799d86"),
                b"password", b"ATHENA.MIT.EDUraeburn", 2, 32
            ),

            # test case 3 / 256 bit
            (
                hb("5c08eb61fdf71e4e4ec3cf6ba1f5512ba7e52ddbc5e5142f708a31e2e62b1e13"),
                b"password", b"ATHENA.MIT.EDUraeburn", 1200, 32
            ),

            # test case 4 / 256 bit
            (
                hb("d1daa78615f287e6a1c8b120d7062a493f98d203e6be49a6adf4fa574b6e64ee"),
                b"password", b'\x12\x34\x56\x78\x78\x56\x34\x12', 5, 32
            ),

            # test case 5 / 256 bit
            (
                hb("139c30c0966bc32ba55fdbf212530ac9c5ec59f1a452f5cc9ad940fea0598ed1"),
                b"X"*64, b"pass phrase equals block size", 1200, 32
            ),

            # test case 6 / 256 bit
            (
                hb("9ccad6d468770cd51b10e6a68721be611a8b4d282601db3b36be9246915ec82a"),
                b"X"*65, b"pass phrase exceeds block size", 1200, 32
            ),

        #
        # from rfc 6070
        #
            (
                hb("0c60c80f961f0e71f3a9b524af6012062fe037a6"),
                b"password", b"salt", 1, 20,
            ),

            (
                hb("ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957"),
                b"password", b"salt", 2, 20,
            ),

            (
                hb("4b007901b765489abead49d926f721d065a429c1"),
                b"password", b"salt", 4096, 20,
            ),

            # just runs too long - could enable if ALL option is set
            ##(
            ##
            ##    unhexlify("eefe3d61cd4da4e4e9945b3d6ba2158c2634e984"),
            ##    "password", "salt", 16777216, 20,
            ##),

            (
                hb("3d2eec4fe41c849b80c8d83662c0e44a8b291a964cf2f07038"),
                b"passwordPASSWORDpassword",
                b"saltSALTsaltSALTsaltSALTsaltSALTsalt",
                4096, 25,
            ),

            (
                hb("56fa6aa75548099dcc37d7f03425e0c3"),
                b"pass\00word", b"sa\00lt", 4096, 16,
            ),

        #
        # from example in http://grub.enbug.org/Authentication
        #
            (
               hb("887CFF169EA8335235D8004242AA7D6187A41E3187DF0CE14E256D85ED"
                  "97A97357AAA8FF0A3871AB9EEFF458392F462F495487387F685B7472FC"
                  "6C29E293F0A0"),
               b"hello",
               hb("9290F727ED06C38BA4549EF7DE25CF5642659211B7FC076F2D28FEFD71"
                  "784BB8D8F6FB244A8CC5C06240631B97008565A120764C0EE9C2CB0073"
                  "994D79080136"),
               10000, 64, "hmac-sha512"
            ),

        #
        # custom
        #
            (
                hb('e248fb6b13365146f8ac6307cc222812'),
                b"secret", b"salt", 10, 16, "hmac-sha1",
            ),
            (
                hb('e248fb6b13365146f8ac6307cc2228127872da6d'),
                b"secret", b"salt", 10, None, "hmac-sha1",
            ),

        ]

    def setUp(self):
        super(Pbkdf2_Test, self).setUp()
        warnings.filterwarnings("ignore", ".*passlib.utils.pbkdf2.*deprecated", DeprecationWarning)

    def test_known(self):
        """test reference vectors"""
        from passlib.utils.pbkdf2 import pbkdf2
        for row in self.pbkdf2_test_vectors:
            correct, secret, salt, rounds, keylen = row[:5]
            prf = row[5] if len(row) == 6 else "hmac-sha1"
            result = pbkdf2(secret, salt, rounds, keylen, prf)
            self.assertEqual(result, correct)

    def test_border(self):
        """test border cases"""
        from passlib.utils.pbkdf2 import pbkdf2
        def helper(secret=b'password', salt=b'salt', rounds=1, keylen=None, prf="hmac-sha1"):
            return pbkdf2(secret, salt, rounds, keylen, prf)
        helper()

        # invalid rounds
        self.assertRaises(ValueError, helper, rounds=-1)
        self.assertRaises(ValueError, helper, rounds=0)
        self.assertRaises(TypeError, helper, rounds='x')

        # invalid keylen
        self.assertRaises(ValueError, helper, keylen=-1)
        self.assertRaises(ValueError, helper, keylen=0)
        helper(keylen=1)
        self.assertRaises(OverflowError, helper, keylen=20*(2**32-1)+1)
        self.assertRaises(TypeError, helper, keylen='x')

        # invalid secret/salt type
        self.assertRaises(TypeError, helper, salt=5)
        self.assertRaises(TypeError, helper, secret=5)

        # invalid hash
        self.assertRaises(ValueError, helper, prf='hmac-foo')
        self.assertRaises(NotImplementedError, helper, prf='foo')
        self.assertRaises(TypeError, helper, prf=5)

    def test_default_keylen(self):
        """test keylen==None"""
        from passlib.utils.pbkdf2 import pbkdf2
        def helper(secret=b'password', salt=b'salt', rounds=1, keylen=None, prf="hmac-sha1"):
            return pbkdf2(secret, salt, rounds, keylen, prf)
        self.assertEqual(len(helper(prf='hmac-sha1')), 20)
        self.assertEqual(len(helper(prf='hmac-sha256')), 32)

    def test_custom_prf(self):
        """test custom prf function"""
        from passlib.utils.pbkdf2 import pbkdf2
        def prf(key, msg):
            return hashlib.md5(key+msg+b'fooey').digest()
        self.assertRaises(NotImplementedError, pbkdf2, b'secret', b'salt', 1000, 20, prf)

#=============================================================================
# eof
#=============================================================================
