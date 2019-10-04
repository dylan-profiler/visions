from collections import namedtuple

import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.models import tenzing_model


relation_conf = namedtuple('relation_conf', ['inferential', 'map'], defaults=[None])


class tenzing_bool(tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False])
    >>> x in tenzing_bool
    True
    """

    @classmethod
    def register_relations(cls):
        from tenzing.core.model.types import tenzing_generic, tenzing_string

        return {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_string: relation_conf(inferential=True, map=[
                    {"true": True, "false": False},
                    {"y": True, "n": False},
                    {"yes": True, "no": False}
                ]
            )
        }

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_categorical_dtype(series):
            return False

        return pdt.is_bool_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(bool)
