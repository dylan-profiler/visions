import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.core.implementations.types.visions_float import test_string_is_float
from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType
from visions.utils.coercion import test_utils


def test_string_is_complex(series):
    coerced_series = test_utils.option_coercion_evaluator(to_complex)(series)

    return coerced_series is not None and not test_string_is_float(series)


def to_complex(series: pd.Series) -> bool:
    return series.apply(complex)


class visions_complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in visions_complex
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_generic, visions_string

        relations = {
            visions_generic: relation_conf(inferential=False),
            visions_string: relation_conf(
                inferential=True,
                relationship=test_string_is_complex,
                transformer=to_complex,
            ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)
