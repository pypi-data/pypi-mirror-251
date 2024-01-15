"""
passlib.utils.decor -- helper decorators & properties
"""
#=============================================================================
# imports
#=============================================================================
# core
from __future__ import absolute_import, division, print_function
import logging
log = logging.getLogger(__name__)
from functools import wraps, update_wrapper
import types
from warnings import warn
# site
# pkg
from passlib.utils.compat import PY3
# local
__all__ = [
    "classproperty",
    "hybrid_method",

    "memoize_single_value",
    "memoized_property",

    "deprecated_function",
    "deprecated_method",
]

#=============================================================================
# class-level decorators
#=============================================================================
class classproperty(object):
    """Function decorator which acts like a combination of classmethod+property (limited to read-only properties)"""

    def __init__(self, func):
        self.im_func = func

    def __get__(self, obj, cls):
        return self.im_func(cls)

    @property
    def __func__(self):
        """py3 compatible alias"""
        return self.im_func

class hybrid_method(object):
    """
    decorator which invokes function with class if called as class method,
    and with object if called at instance level.
    """

    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __get__(self, obj, cls):
        if obj is None:
            obj = cls
        if PY3:
            return types.MethodType(self.func, obj)
        else:
            return types.MethodType(self.func, obj, cls)

#=============================================================================
# memoization
#=============================================================================

def memoize_single_value(func):
    """
    decorator for function which takes no args,
    and memoizes result.  exposes a ``.clear_cache`` method
    to clear the cached value.
    """
    cache = {}

    @wraps(func)
    def wrapper():
        try:
            return cache[True]
        except KeyError:
            pass
        value = cache[True] = func()
        return value

    def clear_cache():
        cache.pop(True, None)
    wrapper.clear_cache = clear_cache

    return wrapper

class memoized_property(object):
    """
    decorator which invokes method once, then replaces attr with result
    """
    def __init__(self, func):
        self.__func__ = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.__func__(obj)
        setattr(obj, self.__name__, value)
        return value

    if not PY3:

        @property
        def im_func(self):
            """py2 alias"""
            return self.__func__

    def clear_cache(self, obj):
        """
        class-level helper to clear stored value (if any).

        usage: :samp:`type(self).{attr}.clear_cache(self)`
        """
        obj.__dict__.pop(self.__name__, None)

    def peek_cache(self, obj, default=None):
        """
        class-level helper to peek at stored value

        usage: :samp:`value = type(self).{attr}.clear_cache(self)`
        """
        return obj.__dict__.get(self.__name__, default)

# works but not used
##class memoized_class_property(object):
##    """function decorator which calls function as classmethod,
##    and replaces itself with result for current and all future invocations.
##    """
##    def __init__(self, func):
##        self.im_func = func
##
##    def __get__(self, obj, cls):
##        func = self.im_func
##        value = func(cls)
##        setattr(cls, func.__name__, value)
##        return value
##
##    @property
##    def __func__(self):
##        "py3 compatible alias"

#=============================================================================
# deprecation
#=============================================================================
def deprecated_function(msg=None, deprecated=None, removed=None, updoc=True,
                        replacement=None, _is_method=False,
                        func_module=None):
    """decorator to deprecate a function.

    :arg msg: optional msg, default chosen if omitted
    :kwd deprecated: version when function was first deprecated
    :kwd removed: version when function will be removed
    :kwd replacement: alternate name / instructions for replacing this function.
    :kwd updoc: add notice to docstring (default ``True``)
    """
    if msg is None:
        if _is_method:
            msg = "the method %(mod)s.%(klass)s.%(name)s() is deprecated"
        else:
            msg = "the function %(mod)s.%(name)s() is deprecated"
        if deprecated:
            msg += " as of Passlib %(deprecated)s"
        if removed:
            msg += ", and will be removed in Passlib %(removed)s"
        if replacement:
            msg += ", use %s instead" % replacement
        msg += "."
    def build(func):
        is_classmethod = _is_method and isinstance(func, classmethod)
        if is_classmethod:
            # NOTE: PY26 doesn't support "classmethod().__func__" directly...
            func = func.__get__(None, type).__func__
        opts = dict(
            mod=func_module or func.__module__,
            name=func.__name__,
            deprecated=deprecated,
            removed=removed,
            )
        if _is_method:
            def wrapper(*args, **kwds):
                tmp = opts.copy()
                klass = args[0] if is_classmethod else args[0].__class__
                tmp.update(klass=klass.__name__, mod=klass.__module__)
                warn(msg % tmp, DeprecationWarning, stacklevel=2)
                return func(*args, **kwds)
        else:
            text = msg % opts
            def wrapper(*args, **kwds):
                warn(text, DeprecationWarning, stacklevel=2)
                return func(*args, **kwds)
        update_wrapper(wrapper, func)
        if updoc and (deprecated or removed) and \
                   wrapper.__doc__ and ".. deprecated::" not in wrapper.__doc__:
            txt = deprecated or ''
            if removed or replacement:
                txt += "\n    "
                if removed:
                    txt += "and will be removed in version %s" % (removed,)
                if replacement:
                    if removed:
                        txt += ", "
                    txt += "use %s instead" % replacement
                txt += "."
            if not wrapper.__doc__.strip(" ").endswith("\n"):
                wrapper.__doc__ += "\n"
            wrapper.__doc__ += "\n.. deprecated:: %s\n" % (txt,)
        if is_classmethod:
            wrapper = classmethod(wrapper)
        return wrapper
    return build

def deprecated_method(msg=None, deprecated=None, removed=None, updoc=True,
                      replacement=None):
    """decorator to deprecate a method.

    :arg msg: optional msg, default chosen if omitted
    :kwd deprecated: version when method was first deprecated
    :kwd removed: version when method will be removed
    :kwd replacement: alternate name / instructions for replacing this method.
    :kwd updoc: add notice to docstring (default ``True``)
    """
    return deprecated_function(msg, deprecated, removed, updoc, replacement,
                               _is_method=True)

#=============================================================================
# eof
#=============================================================================
