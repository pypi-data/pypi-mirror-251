"""test passlib.hosts"""
#=============================================================================
# imports
#=============================================================================
from __future__ import with_statement
# core
import logging; log = logging.getLogger(__name__)
# site
# pkg
from passlib import hosts, hash as hashmod
from passlib.utils import unix_crypt_schemes
from passlib.tests.utils import TestCase
# module

#=============================================================================
# test predefined app contexts
#=============================================================================
class HostsTest(TestCase):
    """perform general tests to make sure contexts work"""
    # NOTE: these tests are not really comprehensive,
    #       since they would do little but duplicate
    #       the presets in apps.py
    #
    #       they mainly try to ensure no typos
    #       or dynamic behavior foul-ups.

    def check_unix_disabled(self, ctx):
        for hash in [
            "",
            "!",
            "*",
            "!$1$TXl/FX/U$BZge.lr.ux6ekjEjxmzwz0",
        ]:
            self.assertEqual(ctx.identify(hash), 'unix_disabled')
            self.assertFalse(ctx.verify('test', hash))

    def test_linux_context(self):
        ctx = hosts.linux_context
        for hash in [
            ('$6$rounds=41128$VoQLvDjkaZ6L6BIE$4pt.1Ll1XdDYduEwEYPCMOBiR6W6'
                'znsyUEoNlcVXpv2gKKIbQolgmTGe6uEEVJ7azUxuc8Tf7zV9SD2z7Ij751'),
            ('$5$rounds=31817$iZGmlyBQ99JSB5n6$p4E.pdPBWx19OajgjLRiOW0itGny'
                 'xDGgMlDcOsfaI17'),
            '$1$TXl/FX/U$BZge.lr.ux6ekjEjxmzwz0',
            'kAJJz.Rwp0A/I',
        ]:
            self.assertTrue(ctx.verify("test", hash))
        self.check_unix_disabled(ctx)

    def test_bsd_contexts(self):
        for ctx in [
            hosts.freebsd_context,
            hosts.openbsd_context,
            hosts.netbsd_context,
        ]:
            for hash in [
                '$1$TXl/FX/U$BZge.lr.ux6ekjEjxmzwz0',
                'kAJJz.Rwp0A/I',
            ]:
                self.assertTrue(ctx.verify("test", hash))
            h1 = "$2a$04$yjDgE74RJkeqC0/1NheSSOrvKeu9IbKDpcQf/Ox3qsrRS/Kw42qIS"
            if hashmod.bcrypt.has_backend():
                self.assertTrue(ctx.verify("test", h1))
            else:
                self.assertEqual(ctx.identify(h1), "bcrypt")
            self.check_unix_disabled(ctx)

    def test_host_context(self):
        ctx = getattr(hosts, "host_context", None)
        if not ctx:
            return self.skipTest("host_context not available on this platform")

        # validate schemes is non-empty,
        # and contains unix_disabled + at least one real scheme
        schemes = list(ctx.schemes())
        self.assertTrue(schemes, "appears to be unix system, but no known schemes supported by crypt")
        self.assertTrue('unix_disabled' in schemes)
        schemes.remove("unix_disabled")
        self.assertTrue(schemes, "should have schemes beside fallback scheme")
        self.assertTrue(set(unix_crypt_schemes).issuperset(schemes))

        # check for hash support
        self.check_unix_disabled(ctx)
        for scheme, hash in [
            ("sha512_crypt", ('$6$rounds=41128$VoQLvDjkaZ6L6BIE$4pt.1Ll1XdDYduEwEYPCMOBiR6W6'
                'znsyUEoNlcVXpv2gKKIbQolgmTGe6uEEVJ7azUxuc8Tf7zV9SD2z7Ij751')),
            ("sha256_crypt", ('$5$rounds=31817$iZGmlyBQ99JSB5n6$p4E.pdPBWx19OajgjLRiOW0itGny'
                 'xDGgMlDcOsfaI17')),
            ("md5_crypt", '$1$TXl/FX/U$BZge.lr.ux6ekjEjxmzwz0'),
            ("des_crypt", 'kAJJz.Rwp0A/I'),
        ]:
            if scheme in schemes:
                self.assertTrue(ctx.verify("test", hash))

#=============================================================================
# eof
#=============================================================================
