import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


# TODO: move to contrib
def is_ordinal_int(s):
    unique_values = list(s.unique())
    return check_consecutive(unique_values) and 2 < len(unique_values) < 10 and 1 in unique_values


# TODO: move to contrib
def is_ordinal_str(s):
    unique_values = s.str.lower().unique()
    return 'a' in unique_values and check_consecutive(list(map(ord, unique_values)))


def to_ordinal(series: pd.Series) -> pd.Series:
    return pd.Series(pd.Categorical(series, categories=sorted(series.unique()), ordered=True))


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
            # TODO: move to contrib
            # tenzing_integer: relation_conf(
            #     inferential=True,
            #     relationship=is_ordinal_int,
            #     transformer=to_ordinal
            # ),
            # TODO: move to contrib
            # tenzing_string: relation_conf(
            #     inferential=True,
            #     relationship=is_ordinal_str,
            #     transformer=to_ordinal
            # ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered
