import numpy as np
import pandas as pd

from visions.relations.relations import InferenceRelation
from visions.types import Integer


def is_unsigned_int(series: pd.Series, state: dict) -> bool:
    # TODO: add coercion, ensure that > uint.MAX raises error
    return series.ge(0).all()


def to_unsigned_int(series: pd.Series) -> pd.Series:
    return series.astype(np.uint64)


def integer_to_count(cls) -> InferenceRelation:
    return InferenceRelation(
        relationship=is_unsigned_int,
        transformer=to_unsigned_int,
        type=cls,
        related_type=Integer,
    )
