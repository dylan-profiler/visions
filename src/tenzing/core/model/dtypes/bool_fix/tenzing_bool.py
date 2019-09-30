import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.models import tenzing_model


class tenzing_boolean(tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([True, False])
        >>> x in tenzing_boolean
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_bool_dtype(series) or series.dtype == "Bool"

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        try:
            return series.astype(bool)
        except ValueError:
            return pd.to_numeric(series).astype("Bool")
