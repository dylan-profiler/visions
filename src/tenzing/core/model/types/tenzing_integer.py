import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.models import tenzing_model


class tenzing_integer(tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_integer_dtype(series):
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            try:
                return series.eq(series.astype(int)).all()
            except (ValueError, TypeError):
                return False
        else:
            return False

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("Int64")
