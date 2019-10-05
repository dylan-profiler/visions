import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def is_unsigned_int(series: pd.Series):
    # TODO: add coercion
    return series.ge(0).all()


class tenzing_count(tenzing_model):
    """**Existing Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1, 4, 10, 20])
    >>> x in tenzing_count
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_integer, tenzing_generic

        relations = {
            # TODO: or inferential=False for integer?
            tenzing_generic: relation_conf(inferential=False),

            # TODO: move to contrib
            # tenzing_integer: relation_conf(
            #     inferential=True,
            #     relationship=is_unsigned_int,
            #     transformer=lambda s: s.astype(np.uint64)
            # ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_unsigned_integer_dtype(series)
