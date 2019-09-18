import pandas as pd
import pandas.api.types as pdt

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_string(tenzing_object):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series(['rubin', 'carter', 'champion'])
        >>> x in tenzing_string
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        if pdt.is_categorical_dtype(series):
            return series.apply(lambda _: False)

        return series.copy().apply(lambda x: type(x) == str)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(str)
