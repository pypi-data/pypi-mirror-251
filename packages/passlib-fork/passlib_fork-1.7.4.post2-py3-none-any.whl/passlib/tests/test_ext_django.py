"""test passlib.ext.django"""
#=============================================================================
# imports
#=============================================================================
# core
from __future__ import absolute_import, division, print_function
import logging; log = logging.getLogger(__name__)
import sys
import re
# site
# pkg
from passlib import apps as _apps, exc, registry
from passlib.apps import django10_context, django14_context, django16_context
from passlib.context import CryptContext
from passlib.ext.django.utils import (
    DJANGO_VERSION, MIN_DJANGO_VERSION, DjangoTranslator, quirks,
)
from passlib.utils.compat import iteritems, get_method_function, u
from passlib.utils.decor import memoized_property
# tests
from passlib.tests.utils import TestCase, TEST_MODE, handler_derived_from
from passlib.tests.test_handlers import get_handler_case
# local
__all__ = [
    "DjangoBehaviorTest",
    "ExtensionBehaviorTest",
    "DjangoExtensionTest",

    "_ExtensionSupport",
    "_ExtensionTest",
]
#=============================================================================
# configure django settings for testcases
#=============================================================================

# whether we have supported django version
has_min_django = DJANGO_VERSION >= MIN_DJANGO_VERSION

# import and configure empty django settings
# NOTE: we don't want to set up entirety of django, so not using django.setup() directly.
#       instead, manually configuring the settings, and setting it up w/ no apps installed.
#       in future, may need to alter this so we call django.setup() after setting
#       DJANGO_SETTINGS_MODULE to a custom settings module w/ a dummy django app.
if has_min_django:
    #
    # initialize django settings manually
    #
    from django.conf import settings, LazySettings

    if not isinstance(settings, LazySettings):
        # this probably means django globals have been configured already,
        # which we don't want, since test cases reset and manipulate settings.
        raise RuntimeError("expected django.conf.settings to be LazySettings: %r" % (settings,))

    # else configure a blank settings instance for the unittests
    if not settings.configured:
        settings.configure()

    #
    # init django apps w/ NO installed apps.
    # NOTE: required for django >= 1.9
    #
    from django.apps import apps
    apps.populate(["django.contrib.contenttypes", "django.contrib.auth"])

# log a warning if tested w/ newer version.
# NOTE: this is mainly here as place to mark what version it was run against before release.
if DJANGO_VERSION >= (3, 2):
    log.info("this release hasn't been tested against Django %r", DJANGO_VERSION)

#=============================================================================
# support funcs
#=============================================================================

# flag for update_settings() to remove specified key entirely
UNSET = object()

def update_settings(**kwds):
    """helper to update django settings from kwds"""
    for k,v in iteritems(kwds):
        if v is UNSET:
            if hasattr(settings, k):
                delattr(settings, k)
        else:
            setattr(settings, k, v)

if has_min_django:
    from django.contrib.auth.models import User

    class FakeUser(User):
        """mock user object for use in testing"""
        # NOTE: this mainly just overrides .save() to test commit behavior.

        # NOTE: .Meta.app_label required for django >= 1.9
        class Meta:
            app_label = __name__

        @memoized_property
        def saved_passwords(self):
            return []

        def pop_saved_passwords(self):
            try:
                return self.saved_passwords[:]
            finally:
                del self.saved_passwords[:]

        def save(self, update_fields=None):
            # NOTE: ignoring update_fields for test purposes
            self.saved_passwords.append(self.password)

def create_mock_setter():
    state = []
    def setter(password):
        state.append(password)
    def popstate():
        try:
            return state[:]
        finally:
            del state[:]
    setter.popstate = popstate
    return setter


def check_django_hasher_has_backend(name):
    """
    check whether django hasher is available;
    or if it should be skipped because django lacks third-party library.
    """
    assert name
    from django.contrib.auth.hashers import make_password
    try:
        make_password("", hasher=name)
        return True
    except ValueError as err:
        if re.match("Couldn't load '.*?' algorithm .* No module named .*", str(err)):
            return False
        raise

#=============================================================================
# work up stock django config
#=============================================================================

def _modify_django_config(kwds, sha_rounds=None):
    """
    helper to build django CryptContext config matching expected setup for stock django deploy.
    :param kwds:
    :param sha_rounds:
    :return:
    """
    # make sure we have dict
    if hasattr(kwds, "to_dict"):
        # type: CryptContext
        kwds = kwds.to_dict()

    # update defaults
    kwds.update(
        # TODO: push this to passlib.apps django contexts
        deprecated="auto",
    )

    # fill in default rounds for current django version, so our sample hashes come back
    # unchanged, instead of being upgraded in-place by check_password().
    if sha_rounds is None and has_min_django:
        from django.contrib.auth.hashers import PBKDF2PasswordHasher
        sha_rounds = PBKDF2PasswordHasher.iterations

    # modify rounds
    if sha_rounds:
        kwds.update(
            django_pbkdf2_sha1__default_rounds=sha_rounds,
            django_pbkdf2_sha256__default_rounds=sha_rounds,
        )

    return kwds

#----------------------------------------------------
# build config dict that matches stock django
#----------------------------------------------------

# XXX: replace this with code that interrogates default django config directly?
#      could then separate out "validation of djangoXX_context objects"
#      and "validation that individual hashers match django".
#      or maybe add a "get_django_context(django_version)" helper to passlib.apps?
if DJANGO_VERSION >= (2, 1):
    stock_config = _modify_django_config(_apps.django21_context)
elif DJANGO_VERSION >= (1, 10):
    stock_config = _modify_django_config(_apps.django110_context)
else:
    # assert DJANGO_VERSION >= (1, 8)
    stock_config = _modify_django_config(_apps.django16_context)

#----------------------------------------------------
# override sample hashes used in test cases
#----------------------------------------------------
from passlib.hash import django_pbkdf2_sha256
sample_hashes = dict(
    django_pbkdf2_sha256=("not a password", django_pbkdf2_sha256
                          .using(rounds=stock_config.get("django_pbkdf2_sha256__default_rounds"))
                          .hash("not a password"))
)

#=============================================================================
# test utils
#=============================================================================

class _ExtensionSupport(object):
    """
    test support funcs for loading/unloading extension.
    this class is mixed in to various TestCase subclasses.
    """
    #===================================================================
    # support funcs
    #===================================================================

    @classmethod
    def _iter_patch_candidates(cls):
        """helper to scan for monkeypatches.

        returns tuple containing:
        * object (module or class)
        * attribute of object
        * value of attribute
        * whether it should or should not be patched
        """
        # XXX: this and assert_unpatched() could probably be refactored to use
        #      the PatchManager class to do the heavy lifting.
        from django.contrib.auth import models, hashers
        user_attrs = ["check_password", "set_password"]
        model_attrs = ["check_password", "make_password"]
        hasher_attrs = ["check_password", "make_password", "get_hasher", "identify_hasher",
                        "get_hashers"]
        objs = [(models, model_attrs),
                (models.User, user_attrs),
                (hashers, hasher_attrs),
        ]
        for obj, patched in objs:
            for attr in dir(obj):
                if attr.startswith("_"):
                    continue
                value = obj.__dict__.get(attr, UNSET) # can't use getattr() due to GAE
                if value is UNSET and attr not in patched:
                    continue
                value = get_method_function(value)
                source = getattr(value, "__module__", None)
                if source:
                    yield obj, attr, source, (attr in patched)

    #===================================================================
    # verify current patch state
    #===================================================================

    def assert_unpatched(self):
        """
        test that django is in unpatched state
        """
        # make sure we aren't currently patched
        mod = sys.modules.get("passlib.ext.django.models")
        self.assertFalse(mod and mod.adapter.patched, "patch should not be enabled")

        # make sure no objects have been replaced, by checking __module__
        for obj, attr, source, patched in self._iter_patch_candidates():
            if patched:
                self.assertTrue(source.startswith("django.contrib.auth."),
                                "obj=%r attr=%r was not reverted: %r" %
                                (obj, attr, source))
            else:
                self.assertFalse(source.startswith("passlib."),
                                "obj=%r attr=%r should not have been patched: %r" %
                                (obj, attr, source))

    def assert_patched(self, context=None):
        """
        helper to ensure django HAS been patched, and is using specified config
        """
        # make sure we're currently patched
        mod = sys.modules.get("passlib.ext.django.models")
        self.assertTrue(mod and mod.adapter.patched, "patch should have been enabled")

        # make sure only the expected objects have been patched
        for obj, attr, source, patched in self._iter_patch_candidates():
            if patched:
                self.assertTrue(source == "passlib.ext.django.utils",
                                "obj=%r attr=%r should have been patched: %r" %
                                (obj, attr, source))
            else:
                self.assertFalse(source.startswith("passlib."),
                                "obj=%r attr=%r should not have been patched: %r" %
                                (obj, attr, source))

        # check context matches
        if context is not None:
            context = CryptContext._norm_source(context)
            self.assertEqual(mod.password_context.to_dict(resolve=True),
                             context.to_dict(resolve=True))

    #===================================================================
    # load / unload the extension (and verify it worked)
    #===================================================================

    _config_keys = ["PASSLIB_CONFIG", "PASSLIB_CONTEXT", "PASSLIB_GET_CATEGORY"]

    def load_extension(self, check=True, **kwds):
        """
        helper to load extension with specified config & patch django
        """
        self.unload_extension()
        if check:
            config = kwds.get("PASSLIB_CONFIG") or kwds.get("PASSLIB_CONTEXT")
        for key in self._config_keys:
            kwds.setdefault(key, UNSET)
        update_settings(**kwds)
        import passlib.ext.django.models
        if check:
            self.assert_patched(context=config)

    def unload_extension(self):
        """
        helper to remove patches and unload extension
        """
        # remove patches and unload module
        mod = sys.modules.get("passlib.ext.django.models")
        if mod:
            mod.adapter.remove_patch()
            del sys.modules["passlib.ext.django.models"]
        # wipe config from django settings
        update_settings(**dict((key, UNSET) for key in self._config_keys))
        # check everything's gone
        self.assert_unpatched()

    #===================================================================
    # eoc
    #===================================================================


# XXX: rename to ExtensionFixture?
# NOTE: would roll this into _ExtensionSupport class;
#       but we have to mix that one into django's TestCase classes as well;
#       and our TestCase class (and this setUp() method) would foul things up.
class _ExtensionTest(TestCase, _ExtensionSupport):
    """
    TestCase mixin which makes sure extension is unloaded before test;
    and make sure it's unloaded after test as well.
    """
    #=============================================================================
    # setup
    #=============================================================================

    def setUp(self):
        super(_ExtensionTest, self).setUp()

        self.require_TEST_MODE("default")

        if not DJANGO_VERSION:
            raise self.skipTest("Django not installed")
        elif not has_min_django:
            raise self.skipTest("Django version too old")

        # reset to baseline, and verify it worked
        self.unload_extension()

        # and do the same when the test exits
        self.addCleanup(self.unload_extension)

    #=============================================================================
    # eoc
    #=============================================================================

#=============================================================================
# extension tests
#=============================================================================

#: static passwords used by DjangoBehaviorTest methods
PASS1 = "toomanysecrets"
WRONG1 = "letmein"


class DjangoBehaviorTest(_ExtensionTest):
    """
    tests model to verify it matches django's behavior.

    running this class verifies the tests correctly assert what Django itself does.

    running the ExtensionBehaviorTest subclass below verifies "passlib.ext.django"
    matches what the tests assert.
    """
    #=============================================================================
    # class attrs
    #=============================================================================

    descriptionPrefix = "verify django behavior"

    #: tracks whether tests should assume "passlib.ext.django" monkeypatch is applied.
    #: (set to True by ExtensionBehaviorTest subclass)
    patched = False

    #: dict containing CryptContext() config which should match current django deploy.
    #: used by tests to verify expected behavior.
    config = stock_config

    # NOTE: if this test fails, it means we're not accounting for
    #       some part of django's hashing logic, or that this is
    #       running against an untested version of django with a new
    #       hashing policy.

    #=============================================================================
    # test helpers
    #=============================================================================

    @memoized_property
    def context(self):
        """
        per-test CryptContext() created from .config.
        """
        return CryptContext._norm_source(self.config)

    def assert_unusable_password(self, user):
        """
        check that user object is set to 'unusable password' constant
        """
        self.assertTrue(user.password.startswith("!"))
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.pop_saved_passwords(), [])

    def assert_valid_password(self, user, hash=UNSET, saved=None):
        """
        check that user object has a usable password hash.
        :param hash: optionally check it has this exact hash
        :param saved: check that mock commit history for user.password matches this list
        """
        if hash is UNSET:
            self.assertNotEqual(user.password, "!")
            self.assertNotEqual(user.password, None)
        else:
            self.assertEqual(user.password, hash)
        self.assertTrue(user.has_usable_password(),
                        "hash should be usable: %r" % (user.password,))
        self.assertEqual(user.pop_saved_passwords(),
                         [] if saved is None else [saved])

    #=============================================================================
    # test hashing interface
    #-----------------------------------------------------------------------------
    # these functions are run against both the actual django code,
    # to verify the assumptions of the unittests are correct;
    # and run against the passlib extension, to verify it matches those assumptions.
    #
    # these tests check the following django methods:
    #   User.set_password()
    #   User.check_password()
    #   make_password() -- 1.4 only
    #   check_password()
    #   identify_hasher()
    #   User.has_usable_password()
    #   User.set_unusable_password()
    #
    # XXX: this take a while to run. what could be trimmed?
    #
    # TODO: add get_hasher() checks where appropriate in tests below.
    #=============================================================================

    def test_extension_config(self):
        """
        test extension config is loaded correctly
        """
        if not self.patched:
            raise self.skipTest("extension not loaded")

        ctx = self.context

        # contexts should match
        from django.contrib.auth.hashers import check_password
        from passlib.ext.django.models import password_context
        self.assertEqual(password_context.to_dict(resolve=True), ctx.to_dict(resolve=True))

        # should have patched both places
        from django.contrib.auth.models import check_password as check_password2
        self.assertEqual(check_password2, check_password)

    def test_default_algorithm(self):
        """
        test django's default algorithm
        """
        ctx = self.context

        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import make_password

        # User.set_password() should use default alg
        user = FakeUser()
        user.set_password(PASS1)
        self.assertTrue(ctx.handler().verify(PASS1, user.password))
        self.assert_valid_password(user)

        # User.check_password() - n/a

        # make_password() should use default alg
        hash = make_password(PASS1)
        self.assertTrue(ctx.handler().verify(PASS1, hash))

        # check_password() - n/a

    def test_empty_password(self):
        """
        test how methods handle empty string as password
        """
        ctx = self.context

        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        # User.set_password() should use default alg
        user = FakeUser()
        user.set_password('')
        hash = user.password
        self.assertTrue(ctx.handler().verify('', hash))
        self.assert_valid_password(user, hash)

        # User.check_password() should return True
        self.assertTrue(user.check_password(""))
        self.assert_valid_password(user, hash)

        # XXX: test make_password() ?

        # TODO: is_password_usable()

        # identify_hasher() -- na

        # check_password() should return True
        self.assertTrue(check_password("", hash))

    def test_unusable_flag(self):
        """
        test how methods handle 'unusable flag' in hash
        """
        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        # sanity check via user.set_unusable_password()
        user = FakeUser()
        user.set_unusable_password()
        self.assert_unusable_password(user)

        # ensure User.set_password() sets unusable flag
        user = FakeUser()
        user.set_password(None)
        self.assert_unusable_password(user)

        # User.check_password() should always fail
        self.assertFalse(user.check_password(None))
        self.assertFalse(user.check_password('None'))
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password(PASS1))
        self.assertFalse(user.check_password(WRONG1))
        self.assert_unusable_password(user)

        # make_password() should also set flag
        self.assertTrue(make_password(None).startswith("!"))

        # check_password() should return False (didn't handle disabled under 1.3)
        self.assertFalse(check_password(PASS1, '!'))

        # identify_hasher() and is_password_usable() should reject it
        self.assertFalse(is_password_usable(user.password))
        self.assertRaises(ValueError, identify_hasher, user.password)

    def test_none_hash_value(self):
        """
        test how methods handle None as hash value
        """
        patched = self.patched

        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        # User.set_password() - n/a

        # User.check_password() - returns False
        user = FakeUser()
        user.password = None
        if quirks.none_causes_check_password_error and not patched:
            # django 2.1+
            self.assertRaises(TypeError, user.check_password, PASS1)
        else:
            self.assertFalse(user.check_password(PASS1))

        self.assertEqual(user.has_usable_password(),
                         quirks.empty_is_usable_password)

        # TODO: is_password_usable()

        # make_password() - n/a

        # check_password() - error
        if quirks.none_causes_check_password_error and not patched:
            self.assertRaises(TypeError, check_password, PASS1, None)
        else:
            self.assertFalse(check_password(PASS1, None))

        # identify_hasher() - error
        self.assertRaises(TypeError, identify_hasher, None)

    def test_empty_hash_value(self):
        """
        test how methods handle empty string as hash value
        """
        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        # User.set_password() - n/a

        # User.check_password()
        # As of django 1.5, blank hash returns False (django issue 18453)
        user = FakeUser()
        user.password = ""
        self.assertFalse(user.check_password(PASS1))

        # verify hash wasn't changed/upgraded during check_password() call
        self.assertEqual(user.password, "")
        self.assertEqual(user.pop_saved_passwords(), [])

        # User.has_usable_password()
        self.assertEqual(user.has_usable_password(), quirks.empty_is_usable_password)

        # TODO: is_password_usable()

        # make_password() - n/a

        # check_password()
        self.assertFalse(check_password(PASS1, ""))

        # identify_hasher() - throws error
        self.assertRaises(ValueError, identify_hasher, "")

    def test_invalid_hash_values(self):
        """
        test how methods handle invalid hash values.
        """
        for hash in [
            "$789$foo",  # empty identifier
        ]:
            with self.subTest(hash=hash):
                self._do_test_invalid_hash_value(hash)

    def _do_test_invalid_hash_value(self, hash):

        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        # User.set_password() - n/a

        # User.check_password()
        # As of django 1.5, invalid hash returns False (side effect of django issue 18453)
        user = FakeUser()
        user.password = hash
        self.assertFalse(user.check_password(PASS1))

        # verify hash wasn't changed/upgraded during check_password() call
        self.assertEqual(user.password, hash)
        self.assertEqual(user.pop_saved_passwords(), [])

        # User.has_usable_password()
        self.assertEqual(user.has_usable_password(), quirks.invalid_is_usable_password)

        # TODO: is_password_usable()

        # make_password() - n/a

        # check_password()
        self.assertFalse(check_password(PASS1, hash))

        # identify_hasher() - throws error
        self.assertRaises(ValueError, identify_hasher, hash)

    def test_available_schemes(self):
        """
        run a bunch of subtests for each hasher available in the default django setup
        (as determined by reading self.context)
        """
        for scheme in self.context.schemes():
            with self.subTest(scheme=scheme):
                self._do_test_available_scheme(scheme)

    def _do_test_available_scheme(self, scheme):
        """
        helper to test how specific hasher behaves.
        :param scheme: *passlib* name of hasher (e.g. "django_pbkdf2_sha256")
        """
        log = self.getLogger()
        ctx = self.context
        patched = self.patched
        setter = create_mock_setter()

        # NOTE: import has to be done w/in method, in case monkeypatching is applied by setUp()
        from django.contrib.auth.hashers import (
            check_password,
            make_password,
            is_password_usable,
            identify_hasher,
        )

        #-------------------------------------------------------
        # setup constants & imports, pick a sample secret/hash combo
        #-------------------------------------------------------
        handler = ctx.handler(scheme)
        log.debug("testing scheme: %r => %r", scheme, handler)
        deprecated = ctx.handler(scheme).deprecated
        assert not deprecated or scheme != ctx.default_scheme()
        try:
            testcase = get_handler_case(scheme)
        except exc.MissingBackendError:
            raise self.skipTest("backend not available")
        assert handler_derived_from(handler, testcase.handler)
        if handler.is_disabled:
            raise self.skipTest("skip disabled hasher")

        # verify that django has a backend available
        # (since our hasher may use different set of backends,
        #  get_handler_case() above may work, but django will have nothing)
        if not patched and not check_django_hasher_has_backend(handler.django_name):
            assert scheme in ["django_bcrypt", "django_bcrypt_sha256", "django_argon2"], \
                "%r scheme should always have active backend" % scheme
            log.warning("skipping scheme %r due to missing django dependency", scheme)
            raise self.skipTest("skip due to missing dependency")

        # find a sample (secret, hash) pair to test with
        try:
            secret, hash = sample_hashes[scheme]
        except KeyError:
            get_sample_hash = testcase("setUp").get_sample_hash
            while True:
                secret, hash = get_sample_hash()
                if secret:  # don't select blank passwords
                    break
        other = 'dontletmein'

        #-------------------------------------------------------
        # User.set_password() - not tested here
        #-------------------------------------------------------

        #-------------------------------------------------------
        # User.check_password()+migration against known hash
        #-------------------------------------------------------
        user = FakeUser()
        user.password = hash

        # check against invalid password
        self.assertFalse(user.check_password(None))
        ##self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password(other))
        self.assert_valid_password(user, hash)

        # check against valid password
        self.assertTrue(user.check_password(secret))

        # check if it upgraded the hash
        # NOTE: needs_update kept separate in case we need to test rounds.
        needs_update = deprecated
        if needs_update:
            self.assertNotEqual(user.password, hash)
            self.assertFalse(handler.identify(user.password))
            self.assertTrue(ctx.handler().verify(secret, user.password))
            self.assert_valid_password(user, saved=user.password)
        else:
            self.assert_valid_password(user, hash)

        # don't need to check rest for most deployments
        if TEST_MODE(max="default"):
            return

        #-------------------------------------------------------
        # make_password() correctly selects algorithm
        #-------------------------------------------------------
        alg = DjangoTranslator().passlib_to_django_name(scheme)
        hash2 = make_password(secret, hasher=alg)
        self.assertTrue(handler.verify(secret, hash2))

        #-------------------------------------------------------
        # check_password()+setter against known hash
        #-------------------------------------------------------
        # should call setter only if it needs_update
        self.assertTrue(check_password(secret, hash, setter=setter))
        self.assertEqual(setter.popstate(), [secret] if needs_update else [])

        # should not call setter
        self.assertFalse(check_password(other, hash, setter=setter))
        self.assertEqual(setter.popstate(), [])

        ### check preferred kwd is ignored (feature we don't currently support fully)
        ##self.assertTrue(check_password(secret, hash, setter=setter, preferred='fooey'))
        ##self.assertEqual(setter.popstate(), [secret])

        # TODO: get_hasher()

        #-------------------------------------------------------
        # identify_hasher() recognizes known hash
        #-------------------------------------------------------
        self.assertTrue(is_password_usable(hash))
        name = DjangoTranslator().django_to_passlib_name(identify_hasher(hash).algorithm)
        self.assertEqual(name, scheme)

    #===================================================================
    # eoc
    #===================================================================

#===================================================================
# extension fidelity tests
#===================================================================

class ExtensionBehaviorTest(DjangoBehaviorTest):
    """
    test that "passlib.ext.django" conforms to behavioral assertions in DjangoBehaviorTest
    """
    descriptionPrefix = "verify extension behavior"

    config = dict(
            schemes="sha256_crypt,md5_crypt,des_crypt",
            deprecated="des_crypt",
            )

    def setUp(self):
        super(ExtensionBehaviorTest, self).setUp()

        # always load extension before each test
        self.load_extension(PASSLIB_CONFIG=self.config)
        self.patched = True

#===================================================================
# extension internal tests
#===================================================================

class DjangoExtensionTest(_ExtensionTest):
    """
    test the ``passlib.ext.django`` plugin
    """
    #===================================================================
    # class attrs
    #===================================================================

    descriptionPrefix = "passlib.ext.django plugin"

    #===================================================================
    # monkeypatch testing
    #===================================================================

    def test_00_patch_control(self):
        """test set_django_password_context patch/unpatch"""

        # check config="disabled"
        self.load_extension(PASSLIB_CONFIG="disabled", check=False)
        self.assert_unpatched()

        # check legacy config=None
        with self.assertWarningList("PASSLIB_CONFIG=None is deprecated"):
            self.load_extension(PASSLIB_CONFIG=None, check=False)
        self.assert_unpatched()

        # try stock django 1.0 context
        self.load_extension(PASSLIB_CONFIG="django-1.0", check=False)
        self.assert_patched(context=django10_context)

        # try to remove patch
        self.unload_extension()

        # patch to use stock django 1.4 context
        self.load_extension(PASSLIB_CONFIG="django-1.4", check=False)
        self.assert_patched(context=django14_context)

        # try to remove patch again
        self.unload_extension()

    def test_01_overwrite_detection(self):
        """test detection of foreign monkeypatching"""
        # NOTE: this sets things up, and spot checks two methods,
        #       this should be enough to verify patch manager is working.
        # TODO: test unpatch behavior honors flag.

        # configure plugin to use sample context
        config = "[passlib]\nschemes=des_crypt\n"
        self.load_extension(PASSLIB_CONFIG=config)

        # setup helpers
        import django.contrib.auth.models as models
        from passlib.ext.django.models import adapter
        def dummy():
            pass

        # mess with User.set_password, make sure it's detected
        orig = models.User.set_password
        models.User.set_password = dummy
        with self.assertWarningList("another library has patched.*User\.set_password"):
            adapter._manager.check_all()
        models.User.set_password = orig

        # mess with models.check_password, make sure it's detected
        orig = models.check_password
        models.check_password = dummy
        with self.assertWarningList("another library has patched.*models:check_password"):
            adapter._manager.check_all()
        models.check_password = orig

    def test_02_handler_wrapper(self):
        """test Hasher-compatible handler wrappers"""
        from django.contrib.auth import hashers

        passlib_to_django = DjangoTranslator().passlib_to_django

        # should return native django hasher if available
        if DJANGO_VERSION > (1, 10):
            self.assertRaises(ValueError, passlib_to_django, "hex_md5")
        else:
            hasher = passlib_to_django("hex_md5")
            self.assertIsInstance(hasher, hashers.UnsaltedMD5PasswordHasher)

        # should return native django hasher
        # NOTE: present but not enabled by default in django as of 2.1
        #       (see _builtin_django_hashers)
        hasher = passlib_to_django("django_bcrypt")
        self.assertIsInstance(hasher, hashers.BCryptPasswordHasher)

        # otherwise should return wrapper
        from passlib.hash import sha256_crypt
        hasher = passlib_to_django("sha256_crypt")
        self.assertEqual(hasher.algorithm, "passlib_sha256_crypt")

        # and wrapper should return correct hash
        encoded = hasher.encode("stub")
        self.assertTrue(sha256_crypt.verify("stub", encoded))
        self.assertTrue(hasher.verify("stub", encoded))
        self.assertFalse(hasher.verify("xxxx", encoded))

        # test wrapper accepts options
        encoded = hasher.encode("stub", "abcd"*4, rounds=1234)
        self.assertEqual(encoded, "$5$rounds=1234$abcdabcdabcdabcd$"
                                  "v2RWkZQzctPdejyRqmmTDQpZN6wTh7.RUy9zF2LftT6")
        self.assertEqual(hasher.safe_summary(encoded),
            {'algorithm': 'sha256_crypt',
             'salt': u('abcdab**********'),
             'rounds': 1234,
             'hash': u('v2RWkZ*************************************'),
             })

        # made up name should throw error
        # XXX: should this throw ValueError instead, to match django?
        self.assertRaises(KeyError, passlib_to_django, "does_not_exist")

    #===================================================================
    # PASSLIB_CONFIG settings
    #===================================================================
    def test_11_config_disabled(self):
        """test PASSLIB_CONFIG='disabled'"""
        # test config=None (deprecated)
        with self.assertWarningList("PASSLIB_CONFIG=None is deprecated"):
            self.load_extension(PASSLIB_CONFIG=None, check=False)
        self.assert_unpatched()

        # test disabled config
        self.load_extension(PASSLIB_CONFIG="disabled", check=False)
        self.assert_unpatched()

    def test_12_config_presets(self):
        """test PASSLIB_CONFIG='<preset>'"""
        # test django presets
        self.load_extension(PASSLIB_CONTEXT="django-default", check=False)
        ctx = django16_context
        self.assert_patched(ctx)

        self.load_extension(PASSLIB_CONFIG="django-1.0", check=False)
        self.assert_patched(django10_context)

        self.load_extension(PASSLIB_CONFIG="django-1.4", check=False)
        self.assert_patched(django14_context)

    def test_13_config_defaults(self):
        """test PASSLIB_CONFIG default behavior"""
        # check implicit default
        from passlib.ext.django.utils import PASSLIB_DEFAULT
        default = CryptContext.from_string(PASSLIB_DEFAULT)
        self.load_extension()
        self.assert_patched(PASSLIB_DEFAULT)

        # check default preset
        self.load_extension(PASSLIB_CONTEXT="passlib-default", check=False)
        self.assert_patched(PASSLIB_DEFAULT)

        # check explicit string
        self.load_extension(PASSLIB_CONTEXT=PASSLIB_DEFAULT, check=False)
        self.assert_patched(PASSLIB_DEFAULT)

    def test_14_config_invalid(self):
        """test PASSLIB_CONFIG type checks"""
        update_settings(PASSLIB_CONTEXT=123, PASSLIB_CONFIG=UNSET)
        self.assertRaises(TypeError, __import__, 'passlib.ext.django.models')

        self.unload_extension()
        update_settings(PASSLIB_CONFIG="missing-preset", PASSLIB_CONTEXT=UNSET)
        self.assertRaises(ValueError, __import__, 'passlib.ext.django.models')

    #===================================================================
    # PASSLIB_GET_CATEGORY setting
    #===================================================================
    def test_21_category_setting(self):
        """test PASSLIB_GET_CATEGORY parameter"""
        # define config where rounds can be used to detect category
        config = dict(
            schemes = ["sha256_crypt"],
            sha256_crypt__default_rounds = 1000,
            staff__sha256_crypt__default_rounds = 2000,
            superuser__sha256_crypt__default_rounds = 3000,
            )
        from passlib.hash import sha256_crypt

        def run(**kwds):
            """helper to take in user opts, return rounds used in password"""
            user = FakeUser(**kwds)
            user.set_password("stub")
            return sha256_crypt.from_string(user.password).rounds

        # test default get_category
        self.load_extension(PASSLIB_CONFIG=config)
        self.assertEqual(run(), 1000)
        self.assertEqual(run(is_staff=True), 2000)
        self.assertEqual(run(is_superuser=True), 3000)

        # test patch uses explicit get_category function
        def get_category(user):
            return user.first_name or None
        self.load_extension(PASSLIB_CONTEXT=config,
                            PASSLIB_GET_CATEGORY=get_category)
        self.assertEqual(run(), 1000)
        self.assertEqual(run(first_name='other'), 1000)
        self.assertEqual(run(first_name='staff'), 2000)
        self.assertEqual(run(first_name='superuser'), 3000)

        # test patch can disable get_category entirely
        def get_category(user):
            return None
        self.load_extension(PASSLIB_CONTEXT=config,
                            PASSLIB_GET_CATEGORY=get_category)
        self.assertEqual(run(), 1000)
        self.assertEqual(run(first_name='other'), 1000)
        self.assertEqual(run(first_name='staff', is_staff=True), 1000)
        self.assertEqual(run(first_name='superuser', is_superuser=True), 1000)

        # test bad value
        self.assertRaises(TypeError, self.load_extension, PASSLIB_CONTEXT=config,
                          PASSLIB_GET_CATEGORY='x')

    #===================================================================
    # eoc
    #===================================================================

#=============================================================================
# eof
#=============================================================================
