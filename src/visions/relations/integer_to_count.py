import numpy as np
import pandas as pd

from visions.types import visions_integer, visions_count
from visions.relations.relations import InferenceRelation


def is_unsigned_int(series: pd.Series):
    # TODO: add coercion, ensure that > uint.MAX raises error
    return series.ge(0).all()


def integer_to_count():
    return InferenceRelation(
        relationship=is_unsigned_int,
        transformer=lambda s: s.astype(np.uint64),
        type=visions_integer,
        related_type=visions_count,
    )
