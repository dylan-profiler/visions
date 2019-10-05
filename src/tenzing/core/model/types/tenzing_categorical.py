import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.core.model.types import tenzing_string


class tenzing_categorical(tenzing_model):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """

    @classmethod
    def get_relations(cls) -> dict:
        from tenzing.core.model.types import tenzing_generic

        return {
            tenzing_generic: relation_conf(inferential=False),
            # TODO: contrib
            # tenzing_string: relation_conf(inferential=True, relationship=lambda s: s, transformer=lambda s: s)
        }

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series)
