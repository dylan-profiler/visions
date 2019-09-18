import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_complex(tenzing_generic):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in tenzing_complex
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        if pdt.is_complex_dtype(series):
            mask = series[super_mask].apply(lambda _: True)
        else:
            mask = series[super_mask].apply(lambda _: False)

        return super_mask & mask
        # return series.apply(lambda x: issubclass(type(x), np.complex_))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("complex")
