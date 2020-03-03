import numpy as np
import pandas as pd
from visions import visions_integer

from visions.core.model.relations import InferenceRelation


def is_unsigned_int(series: pd.Series):
    # TODO: add coercion, ensure that > uint.MAX raises error
    return series.ge(0).all()


def integer_to_count(cls) -> InferenceRelation:
    return InferenceRelation(
        relationship=is_unsigned_int,
        transformer=lambda s: s.astype(np.uint64),
        type=cls,
        related_type=visions_integer,
    )
