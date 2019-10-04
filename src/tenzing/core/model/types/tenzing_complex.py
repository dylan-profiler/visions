import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_complex(tenzing_model):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in tenzing_complex
        True
    """

    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in tenzing_complex
    True
    """

    @classmethod
    def register_relations(cls):
        from tenzing.core.model.types import tenzing_generic

        relations = {
            tenzing_generic: relation_conf(inferential=False)
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("complex")
