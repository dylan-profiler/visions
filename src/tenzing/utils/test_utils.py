
"""
test_utils.py
====================================
A selection of testing utilities for tenzing.
"""


def option_coercion_evaluator(method):
    """A coercion test evaluator

    Evaluates a coercion method and optionally returns the coerced series.

    Parameters
    ----------
    method : func
        A method coercing a Series to another type.

    Returns
    -------
    Option[Series]
        The coerced series if the coercion succeeds otherwise None.

    """
    # Returns Option[result] where result is the coercion of a series from method
    def f(series):
        try:
            return method(series)
        except (ValueError, TypeError):
            return None
    return f


def coercion_test(method):
    """A coercion test generator

    Creates a coercion test based on a provided coercion method.

    Parameters
    ----------
    method : func
        A method coercing a Series to another type.

    Returns
    -------
    bool
        Whether the coercion failed or was succesful.

    """
    # Returns True or False if the coercion succeeds
    tester = option_coercion_evaluator(method)

    def f(series):
        result = tester(series)
        return True if result is not None else False
    return f


def coercion_equality_test(method):
    """A coercion equality test generator

    Creates a coercion test based on a provided coercion method which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a series without necessarily changing the data, for example,
    when converting an integer to a float.

    Parameters
    ----------
    method : func
        A method coercing a Series to another type.

    Returns
    -------
    bool
        Whether the coercion failed or was succesful.

    """
    tester = option_coercion_evaluator(method)

    def f(series):
        result = tester(series)
        return False if result is None else series.eq(result).all()
    return f
