import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_categorical(tenzing_generic):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([True, False, 1], dtype='category')
        >>> x in tenzing_categorical
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        if pdt.is_categorical_dtype(series):
            return series.apply(lambda _: True)
        else:
            return series.apply(lambda _: False)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("category")
