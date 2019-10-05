import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_int(s):
    unique_values = s.unique()
    return check_consecutive(unique_values) and 2 < len(unique_values) < 10 and 1 in unique_values


def is_ordinal_str(s):
    unique_values = s.str.lower().unique()
    return 'a' in unique_values and check_consecutive(list(map(ord, unique_values)))


class tenzing_ordinal(tenzing_model):
    """**Ordinal** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
    >>> x in tenzing_ordinal
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_categorical, tenzing_string, tenzing_integer

        relations = {
            tenzing_categorical: relation_conf(inferential=False),
            tenzing_integer: relation_conf(inferential=True, relationship=is_ordinal_int),
            tenzing_string: relation_conf(inferential=True, relationship=is_ordinal_str),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.Series(pd.Categorical(series, categories=sorted(series.unique()), ordered=True))
