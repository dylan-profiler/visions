import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


class tenzing_complex(tenzing_generic):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in tenzing_complex
    True
    """

    @classmethod
    def contains_op(cls, series):
        return not series.empty and pdt.is_complex_dtype(series)

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("complex")
