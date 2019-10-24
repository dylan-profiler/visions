import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


class visions_complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.core.models.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in visions_complex
        True
    """

    """**Complex** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in visions_complex
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_generic

        relations = {visions_generic: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)
