import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_object(tenzing_generic):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in tenzing_object
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        # TODO: mask super()?
        if pdt.is_object_dtype(series[super_mask]):
            mask = series[super_mask].apply(lambda _: True)
        else:
            mask = series[super_mask].apply(lambda _: False)
        return super_mask & mask
        # return series.apply(lambda x: issubclass(type(x), np.object_))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("object")
