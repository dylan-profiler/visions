import pandas as pd

from visions.relations.relations import InferenceRelation
from visions.relations.relations_utils import values_are_consecutive
from visions.types.ordinal import to_ordinal
from visions.utils import func_nullable_series_contains


@func_nullable_series_contains
def is_ordinal_cat(series: pd.Series, state: dict) -> bool:
    initial_element = "a"
    s = series.astype(str)
    if s.str.len().max() == 1:
        distinct_values = list(s.str.lower().unique())
        return initial_element in distinct_values and values_are_consecutive(
            list(map(ord, distinct_values))
        )
    else:
        return False


def categorical_to_ordinal(cls) -> InferenceRelation:
    from visions.types import Categorical

    return InferenceRelation(
        cls, Categorical, relationship=is_ordinal_cat, transformer=to_ordinal
    )
