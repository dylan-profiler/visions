import numpy as np
import pandas as pd

from tenzing.core.model.model_relation import relation_conf


def is_unsigned_int(series: pd.Series):
    # TODO: add coercion, ensure that > uint.MAX raises error
    return series.ge(0).all()


def integer_to_count():
    return relation_conf(
        inferential=True,
        relationship=is_unsigned_int,
        transformer=lambda s: s.astype(np.uint64)
    )
