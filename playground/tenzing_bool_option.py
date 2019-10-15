import pandas as pd

from visions.core.models import visions_model


class visions_bool_option(visions_model):
    """**Nullable Boolean** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([True, False, np.nan])
    >>> x in visions_bool_option
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "Bool"

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("Bool")
