import numpy as np
import pandas as pd
from tenzing.core.model.models import tenzing_model


class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_generic
    True
    """

    @classmethod
    def get_relations(cls) -> dict:
        return {}

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return True

    @classmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        return series
