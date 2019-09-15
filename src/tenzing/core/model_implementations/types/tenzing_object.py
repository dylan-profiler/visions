import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


class tenzing_object(tenzing_generic):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """

    @classmethod
    def contains_op(cls, series):
        return not series.empty and pdt.is_object_dtype(series) and not series.hasnans

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("object")
