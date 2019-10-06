import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


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
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_unsigned_integer_dtype(series)
