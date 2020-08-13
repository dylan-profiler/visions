import functools
import os
import sys
import warnings


def suppress_warnings(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return inner


def discard_stderr(func):
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
    Only known way to get rid of sys output when wkt.loads hits a bad value"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sys.stderr = open(os.devnull, "w")
        res = func(*args, **kwargs)
        sys.stderr = sys.__stderr__
        return res

    return wrapper
