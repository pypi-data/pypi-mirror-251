"""
test passlib.ext.django against django source tests
"""
#=============================================================================
# imports
#=============================================================================
from __future__ import absolute_import, division, print_function
# core
import logging; log = logging.getLogger(__name__)
# site
# pkg
from passlib.utils.compat import suppress_cause
from passlib.ext.django.utils import DJANGO_VERSION, DjangoTranslator, _PasslibHasherWrapper
# tests
from passlib.tests.utils import TestCase, TEST_MODE
from .test_ext_django import (
    has_min_django, stock_config, _ExtensionSupport,
)
if has_min_django:
    from .test_ext_django import settings
# local
__all__ = [
    "HashersTest",
]
#=============================================================================
# HashersTest --
# hack up the some of the real django tests to run w/ extension loaded,
# to ensure we mimic their behavior.
# however, the django tests were moved out of the package, and into a source-only location
# as of django 1.7. so we disable tests from that point on unless test-runner specifies
#=============================================================================

#: ref to django unittest root module (if found)
test_hashers_mod = None

#: message about why test module isn't present (if not found)
hashers_skip_msg = None

#----------------------------------------------------------------------
# try to load django's tests/auth_tests/test_hasher.py module,
# or note why we failed.
#----------------------------------------------------------------------
if TEST_MODE(max="quick"):
    hashers_skip_msg = "requires >= 'default' test mode"

elif has_min_django:
    import os
    import sys
    source_path = os.environ.get("PASSLIB_TESTS_DJANGO_SOURCE_PATH")

    if source_path:
        if not os.path.exists(source_path):
            raise EnvironmentError("django source path not found: %r" % source_path)
        if not all(os.path.exists(os.path.join(source_path, name))
                   for name in ["django", "tests"]):
            raise EnvironmentError("invalid django source path: %r" % source_path)
        log.info("using django tests from source path: %r", source_path)
        tests_path = os.path.join(source_path, "tests")
        sys.path.insert(0, tests_path)
        try:
            from auth_tests import test_hashers as test_hashers_mod
        except ImportError as err:
            raise suppress_cause(
                EnvironmentError("error trying to import django tests "
                                 "from source path (%r): %r" %
                                 (source_path, err)))
        finally:
            sys.path.remove(tests_path)

    else:
        hashers_skip_msg = "requires PASSLIB_TESTS_DJANGO_SOURCE_PATH to be set"

        if TEST_MODE("full"):
            # print warning so user knows what's happening
            sys.stderr.write("\nWARNING: $PASSLIB_TESTS_DJANGO_SOURCE_PATH is not set; "
                             "can't run Django's own unittests against passlib.ext.django\n")

elif DJANGO_VERSION:
    hashers_skip_msg = "django version too old"

else:
    hashers_skip_msg = "django not installed"

#----------------------------------------------------------------------
# if found module, create wrapper to run django's own tests,
# but with passlib monkeypatched in.
#----------------------------------------------------------------------
if test_hashers_mod:
    from django.core.signals import setting_changed
    from django.dispatch import receiver
    from django.utils.module_loading import import_string
    from passlib.utils.compat import get_unbound_method_function

    class HashersTest(test_hashers_mod.TestUtilsHashPass, _ExtensionSupport):
        """
        Run django's hasher unittests against passlib's extension
        and workalike implementations
        """

        #==================================================================
        # helpers
        #==================================================================

        # port patchAttr() helper method from passlib.tests.utils.TestCase
        patchAttr = get_unbound_method_function(TestCase.patchAttr)

        #==================================================================
        # custom setup
        #==================================================================
        def setUp(self):
            #---------------------------------------------------------
            # install passlib.ext.django adapter, and get context
            #---------------------------------------------------------
            self.load_extension(PASSLIB_CONTEXT=stock_config, check=False)
            from passlib.ext.django.models import adapter
            context = adapter.context

            #---------------------------------------------------------
            # patch tests module to use our versions of patched funcs
            # (which should be installed in hashers module)
            #---------------------------------------------------------
            from django.contrib.auth import hashers
            for attr in ["make_password",
                         "check_password",
                         "identify_hasher",
                         "is_password_usable",
                         "get_hasher"]:
                self.patchAttr(test_hashers_mod, attr, getattr(hashers, attr))

            #---------------------------------------------------------
            # django tests expect empty django_des_crypt salt field
            #---------------------------------------------------------
            from passlib.hash import django_des_crypt
            self.patchAttr(django_des_crypt, "use_duplicate_salt", False)

            #---------------------------------------------------------
            # install receiver to update scheme list if test changes settings
            #---------------------------------------------------------
            django_to_passlib_name = DjangoTranslator().django_to_passlib_name

            @receiver(setting_changed, weak=False)
            def update_schemes(**kwds):
                if kwds and kwds['setting'] != 'PASSWORD_HASHERS':
                    return
                assert context is adapter.context
                schemes = [
                    django_to_passlib_name(import_string(hash_path)())
                    for hash_path in settings.PASSWORD_HASHERS
                ]
                # workaround for a few tests that only specify hex_md5,
                # but test for django_salted_md5 format.
                if "hex_md5" in schemes and "django_salted_md5" not in schemes:
                    schemes.append("django_salted_md5")
                schemes.append("django_disabled")
                context.update(schemes=schemes, deprecated="auto")
                adapter.reset_hashers()

            self.addCleanup(setting_changed.disconnect, update_schemes)

            update_schemes()

            #---------------------------------------------------------
            # need password_context to keep up to date with django_hasher.iterations,
            # which is frequently patched by django tests.
            #
            # HACK: to fix this, inserting wrapper around a bunch of context
            #       methods so that any time adapter calls them,
            #       attrs are resynced first.
            #---------------------------------------------------------

            def update_rounds():
                """
                sync django hasher config -> passlib hashers
                """
                for handler in context.schemes(resolve=True):
                    if 'rounds' not in handler.setting_kwds:
                        continue
                    hasher = adapter.passlib_to_django(handler)
                    if isinstance(hasher, _PasslibHasherWrapper):
                        continue
                    rounds = getattr(hasher, "rounds", None) or \
                             getattr(hasher, "iterations", None)
                    if rounds is None:
                        continue
                    # XXX: this doesn't modify the context, which would
                    #      cause other weirdness (since it would replace handler factories completely,
                    #      instead of just updating their state)
                    handler.min_desired_rounds = handler.max_desired_rounds = handler.default_rounds = rounds

            _in_update = [False]

            def update_wrapper(wrapped, *args, **kwds):
                """
                wrapper around arbitrary func, that first triggers sync
                """
                if not _in_update[0]:
                    _in_update[0] = True
                    try:
                        update_rounds()
                    finally:
                        _in_update[0] = False
                return wrapped(*args, **kwds)

            # sync before any context call
            for attr in ["schemes", "handler", "default_scheme", "hash",
                         "verify", "needs_update", "verify_and_update"]:
                self.patchAttr(context, attr, update_wrapper, wrap=True)

            # sync whenever adapter tries to resolve passlib hasher
            self.patchAttr(adapter, "django_to_passlib", update_wrapper, wrap=True)

        def tearDown(self):
            # NOTE: could rely on addCleanup() instead, but need py26 compat
            self.unload_extension()
            super(HashersTest, self).tearDown()

        #==================================================================
        # skip a few methods that can't be replicated properly
        # *want to minimize these as much as possible*
        #==================================================================

        _OMIT = lambda self: self.skipTest("omitted by passlib")

        # XXX: this test registers two classes w/ same algorithm id,
        #      something we don't support -- how does django sanely handle
        #      that anyways? get_hashers_by_algorithm() should throw KeyError, right?
        test_pbkdf2_upgrade_new_hasher = _OMIT

        # TODO: support wrapping django's harden-runtime feature?
        #       would help pass their tests.
        test_check_password_calls_harden_runtime = _OMIT
        test_bcrypt_harden_runtime = _OMIT
        test_pbkdf2_harden_runtime = _OMIT

        #==================================================================
        # eoc
        #==================================================================

else:
    # otherwise leave a stub so test log tells why test was skipped.

    class HashersTest(TestCase):

        def test_external_django_hasher_tests(self):
            """external django hasher tests"""
            raise self.skipTest(hashers_skip_msg)

#=============================================================================
# eof
#=============================================================================
