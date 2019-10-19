import warnings


def suppress_warnings(func):
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return inner
