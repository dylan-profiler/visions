import numpy as np

# def inf(Cls):
#     """
#     >>> @inf
#     >>> class tenzing_integer(tenzing_model):
#     >>>     pass
#     """
#     class NewCls(object):
#         pass
#
#     return NewCls


class infMixin:
    """Mixin adding infinite value support to tenzing types

    When creating a custom Tenzing type simply inherit from infMixin to add
    automatic support for infinite values.

    >>> @singleton.singleton_object
    >>> class tenzing_integer(infMixin, tenzing_model):
    >>>     // Implementation

    """
    # TODO: is this used?
    is_option = True

    # Todo: is this even used?
    def get_series(self, series):
        try:
            if np.issubdtype(series.dtype, np.number):
                return series[~np.isinf(series)]
            else:
                return series
        except TypeError:
            return series

    def cast_op(self, series, operation=None):
        operation = operation if operation is not None else super().cast_op
        notinf_series = self.get_series(series)
        # TODO: copy?
        return operation(notinf_series)

    def contains_op(self, series):
        notinf_series = self.get_series(series)
        return super().contains_op(notinf_series)

    def summarization_op(self, series):
        idx = np.isinf(series)
        summary = super().summarization_op(series[~idx])

        summary['inf_count'] = idx.values.sum()
        summary['perc_inf'] = summary['inf_count'] / series.shape[0] if series.shape[0] > 0 else 0
        return summary
