import pandas as pd
from visions.core.model.type import VisionsBaseType


class visions_generic(VisionsBaseType):
    """**Generic** implementation of :class:`visions.core.models.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions_generic
        True
    """

    @classmethod
    def get_relations(cls) -> dict:
        return {}

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return True
