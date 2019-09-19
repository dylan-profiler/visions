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
        super_mask = super().mask(series)

        if not super_mask.any():
            return super_mask

        if pdt.is_categorical_dtype(series[super_mask]):
            mask = series[super_mask].apply(lambda _: False)
        else:
            mask = series[super_mask].copy().apply(lambda x: type(x) == str)
        return super_mask & mask

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(str)
