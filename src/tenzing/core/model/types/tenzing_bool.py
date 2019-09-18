import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_bool(tenzing_generic):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([True, False, np.nan])
        >>> x in tenzing_bool
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)

        # TODO: fix
        if pdt.is_categorical_dtype(series):
            return series.apply(lambda _: False)

        if pdt.is_bool_dtype(series):
            return super_mask & series.apply(lambda _: True)

        return super_mask & series.apply(lambda x: type(x) == bool)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not super().contains_op(series):
            return False
        return cls.mask(series).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(bool)
