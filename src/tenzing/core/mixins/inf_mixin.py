import numpy as np


class infMixin:
    """Mixin adding infinite value support to tenzing types

    When creating a custom Tenzing type simply inherit from infMixin to add
    automatic support for infinite values.

    >>> @singleton.singleton_object
    >>> class tenzing_integer(infMixin, tenzing_model):
    >>>     // Implementation

    """
    is_option = True

    def cast(self, series, operation=None):
        operation = operation if operation is not None else self.cast_op

        idx = series.isinf()
        if idx.any():
            result = series.copy()
            result[~idx] = operation(series[~idx])
        else:
            result = operation(series)

        return result

    def get_series(self, series):
        try:
            if np.issubdtype(series.dtype, np.number):
                return series[~np.isinf(series)]
            else:
                return series
        except TypeError:
            return series

    def __contains__(self, series):
        notinf_series = self.get_series(series)
        return self.contains_op(notinf_series)

    def summarization_op(self, series):
        idx = np.isinf(series)
        summary = super().summarization_op(series[~idx])

        summary['inf_count'] = idx.values.sum()
        summary['perc_inf'] = summary['inf_count'] / series.shape[0] if series.shape[0] > 0 else 0
        return summary
