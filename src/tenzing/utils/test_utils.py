def coercion_test(method):
    def f(series):
        try:
            method(series)
        except (ValueError, TypeError):
            return False
        return True

    return f
