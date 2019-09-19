import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_integer(tenzing_generic):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        # TODO: first apply super mask, then check rest
        series = series[super_mask]

        if pdt.is_integer_dtype(series):
            mask = pd.Series([True] * len(series), name=series.name)

        # Note: this is required to support series with np.inf (as their representation is float)
        elif pdt.is_float_dtype(series):
            mask = series.eq(series.astype(int))
        else:
            mask = pd.Series([False] * len(series), name=series.name)

        return super_mask & mask

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(int)
