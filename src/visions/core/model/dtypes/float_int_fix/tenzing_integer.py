import pandas.api.types as pdt
import pandas as pd

from visions.core.model.models import tenzing_model


class tenzing_integer(tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_integer_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        try:
            return series.astype(int)
        except ValueError:
            return series.astype("Int64")
