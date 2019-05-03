
def option_coercion_evaluator(method):
    # Returns Option[result] where result is the coercion of a series from method
    def f(series):
        try:
            return method(series)
        except (ValueError, TypeError):
            return None
    return f


def coercion_test(method):
    # Returns True or False if the coercion succeeds
    tester = option_coercion_evaluator(method)

    def f(series):
        result = tester(series)
        return True if result is not None else False
    return f


def coercion_equality_test(method):
    # Returns True if the coercion succeeds and the coerced series has the same
    # underlying data as the original series (i.e. integer == float)
    tester = option_coercion_evaluator(method)

    def f(series):
        result = tester(series)
        return False if result is None else series.eq(result).all()
    return f
