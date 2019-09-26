import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_bool_option(tenzing_model):
    """**Nullable Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False, np.nan])
    >>> x in tenzing_bool_option
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == 'Bool'

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype('Bool')
