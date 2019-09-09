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
        return series[~np.isinf(series)]

    def __contains__(self, series):
        idx = series.isinf()
        notinf_series = series[~idx].infer_objects() if idx.any() else series
        return self.contains_op(notinf_series)

    def summarize(self, series):
        idx = np.isinf(series)
        summary = self.summarization_op(series[~idx])

        summary['inf_count'] = idx.values.sum()
        summary['perc_inf'] = summary['inf_count'] / series.shape[0] if series.shape[0] > 0 else 0
        # summary['n_records'] = series.shape[0]
        return summary
