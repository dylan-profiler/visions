import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.core.model.types import tenzing_string
from tenzing.utils.coercion import test_utils


class tenzing_datetime(tenzing_model):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_datetime
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_generic

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_string: relation_conf(relationship=test_utils.coercion_test(lambda s: pd.to_datetime(s)), inferential=True),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)
