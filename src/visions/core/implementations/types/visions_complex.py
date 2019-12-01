import pandas.api.types as pdt
import pandas as pd
import numpy as np
from typing import Sequence

from visions.core.implementations.types.visions_float import test_string_is_float
from visions.core.model.relations import (
    IdentityRelation,
    InferenceRelation,
)
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType
from visions.utils.coercion import test_utils


def test_string_is_complex(series) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(to_complex)(series)

    return coerced_series is not None and not test_string_is_float(series)


def to_complex(series: pd.Series) -> bool:
    return series.apply(complex)


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_generic, visions_string

    relations = [
        IdentityRelation(visions_complex, visions_generic),
        InferenceRelation(
            visions_complex,
            visions_string,
            relationship=test_string_is_complex,
            transformer=to_complex,
        ),
    ]
    return relations


class visions_complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in visions_complex
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_complex_dtype(series)
