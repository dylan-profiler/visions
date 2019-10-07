import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import tenzing_model


class tenzing_object(tenzing_model):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import tenzing_generic

        relations = {tenzing_generic: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_object_dtype(series)
