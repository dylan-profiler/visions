from typing import Sequence

import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.types.float import test_is_float
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils


def test_string_is_complex(series) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(to_complex)(series)
    return coerced_series is not None and not test_is_float(series)


def to_complex(series: pd.Series) -> bool:
    return series.apply(complex)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=test_string_is_complex, transformer=to_complex
        ),
    ]
    return relations


class Complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in visions.Complex
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)
